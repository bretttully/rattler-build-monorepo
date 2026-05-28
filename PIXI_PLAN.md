# PIXI_PLAN.md — pixi-build monorepo blueprint

End-to-end trial of a rust + python + apps monorepo built and orchestrated with `pixi` + `pixi-build`. All findings below are grounded in the working code in this repo: 4 rust crates in 2 groups, 2 PyO3 cdylibs, 2 pure-Python libs, 2 apps with divergent transitive closures.

## TL;DR — recommended pattern

`pixi-build` with a **single root Cargo workspace** is sufficient for this shape. The feared `extension-module` feature unification across PyO3 cdylibs and pure-Rust rlibs did **not** materialise — `cargo build` resolved features cleanly within one workspace. The two-workspace split (separate `python/Cargo.toml`) is **not required** for this pattern; reach for it only if a concrete feature-graph problem appears later.

Per-package metadata lives in each leaf's `pyproject.toml` (`[tool.pixi.package.*]`); the root `pixi.toml` lists only top-of-graph apps in `[dependencies]` and the workspace pulls the rest transitively.

## What was validated

| Capability | Status |
|---|---|
| Multi-crate rust group (e.g. `fastthing-{core,stats}`) building together | ✓ |
| PyO3 cdylib re-exporting from multiple rust crates in the group | ✓ |
| Pure-Python lib depending on a PyO3 cdylib via path source dep | ✓ |
| Pure-Python lib depending on **two** PyO3 cdylibs (cross-group) | ✓ |
| Two apps with divergent transitive closures resolving independently | ✓ |
| `pixi-build-python` auto-detecting maturin from `[build-system]`, provisioning rust toolchain | ✓ |
| Editable installs picking up live source edits | ✓ |
| `pixi install` stable across re-runs (lockfile hash unchanged) | ✓ |
| `cargo test --workspace` across single workspace with mixed rlib + cdylib | ✓ |
| Single Cargo workspace covering both `rust/` and `python/` cdylibs | ✓ |

## Manifest patterns that worked

### Root `pixi.toml`

```toml
[workspace]
name = "..."
channels = ["https://prefix.dev/pixi-build-backends", "https://prefix.dev/conda-forge"]
platforms = ["linux-64", "osx-arm64"]
preview = ["pixi-build"]

[dependencies]
# Top-of-graph apps pull every leaf transitively.
cli_simple = { path = "apps/cli_simple" }
cli_full = { path = "apps/cli_full" }
# Workspace tooling not provided by any source package.
pytest = "*"
ruff = "*"

[tasks]
test = "pytest libs apps --import-mode=importlib"
test-rust = "cargo test --workspace"
lint = "ruff format --check . && ruff check ."
```

Note `--import-mode=importlib` on the pytest invocation — see [gotchas](#gotchas-encountered).

### Root `Cargo.toml` — single workspace covers both rust/ and python/

```toml
[workspace]
members = [
    "rust/fastthing-core",
    "rust/fastthing-stats",
    "rust/geocompute-core",
    "rust/geocompute-tiles",
    "python/fastthing",
    "python/geocompute",
]
resolver = "2"
```

### PyO3 cdylib — `python/fastthing/pyproject.toml`

```toml
[build-system]
build-backend = "maturin"
requires = ["maturin>=1.7,<2.0"]

[project]
name = "fastthing"
version = "0.1.0"
requires-python = ">=3.12"

[tool.maturin]
features = ["pyo3/extension-module"]
module-name = "fastthing"

[tool.pixi.package.build.backend]
channels = ["https://prefix.dev/pixi-build-backends", "https://prefix.dev/conda-forge"]
name = "pixi-build-python"
version = "0.4.*"

[tool.pixi.package.host-dependencies]
maturin = ">=1.7,<2.0"
python = "3.12.*"

[tool.pixi.package.run-dependencies]
python = "3.12.*"
```

`pixi-build-python` reads the standard PEP 517 `[build-system]` block, detects maturin, and provisions the rust toolchain automatically. No explicit `compilers = ["rust"]` field is needed.

### PyO3 cdylib — `python/fastthing/Cargo.toml`

```toml
[package]
name = "fastthing"
version = "0.1.0"
edition = "2021"

[lib]
name = "fastthing"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.22", features = ["extension-module"] }
fastthing-core = { path = "../../rust/fastthing-core" }
fastthing-stats = { path = "../../rust/fastthing-stats" }
```

### Pure-Python lib that depends on a PyO3 cdylib — `libs/slowthing/pyproject.toml`

```toml
[build-system]
build-backend = "hatchling.build"
requires = ["hatchling"]

[project]
name = "slowthing"
version = "0.1.0"
requires-python = ">=3.12"

[tool.pixi.package.build.backend]
channels = ["https://prefix.dev/pixi-build-backends", "https://prefix.dev/conda-forge"]
name = "pixi-build-python"
version = "0.4.*"

[tool.pixi.package.host-dependencies]
hatchling = "*"
python = "3.12.*"

[tool.pixi.package.run-dependencies]
python = "3.12.*"
fastthing = { path = "../../python/fastthing" }
```

Cross-package source deps go in `[tool.pixi.package.run-dependencies]` using `path = "..."`. Same pattern works for apps depending on libs, and libs depending on multiple PyO3 packages (`libs/geoanalysis` in this repo depends on both `fastthing` and `geocompute`).

## Two-workspace split — when (if ever) to reach for it

This trial deliberately started with a single workspace covering both pure-Rust crates and PyO3 cdylibs to test whether the feared feature-unification problem (where `pyo3/extension-module` could leak into pure-Rust crates that don't need it) actually bites. **It didn't.** All six crates compile cleanly in one workspace, the PyO3 extension feature is scoped to the cdylib targets only, and `cargo test --workspace` runs all unit tests without unification issues.

Conclusion: **prefer a single workspace** unless a concrete failure mode emerges. Reasons to escalate to two workspaces would be:

- A pure-Rust crate gets unintended PyO3 symbols pulled in at link time (i.e. an actual unification regression in a future cargo version).
- A pure-Rust crate needs to publish to crates.io independently and you want to keep its workspace clean of PyO3-specific lockfile entries.
- The PyO3 cdylib set wants a different resolver mode than the pure-Rust set.

If you do need to split, the layout is:

```
Cargo.toml          # members = ["rust/*"]
python/Cargo.toml   # members = ["python/*-cdylib"]
```

Sub-crate `Cargo.toml` files reference cross-workspace pure-Rust crates by relative path (e.g. `../../rust/fastthing-core`). Both workspaces declare `resolver = "2"`.

## Task graph

| Task | What it does |
|---|---|
| `pixi install` | Solves the workspace; builds every source package via `pixi-build-python`. On a clean checkout this pulls the rust toolchain. |
| `pixi run test` | `pytest libs apps --import-mode=importlib` — collects across all sub-packages. |
| `pixi run test-rust` | `cargo test --workspace` — runs every crate's unit tests. |
| `pixi run lint` | `ruff format --check` + `ruff check`. |
| `pixi run demo-simple` | Runs the math-only app. Exercises the lighter transitive closure (slowthing → fastthing). |
| `pixi run demo-full` | Runs the geo+math app. Exercises the full closure (geoanalysis → fastthing + geocompute). |

## CI implications

- Single workflow can drive everything: checkout → `prefix-dev/setup-pixi` → `pixi run lint && pixi run test && pixi run test-rust`.
- Per-package conda artifacts already live under `.pixi/artifacts-v0/<package>/`; shipping them is a matter of plumbing them to a channel (or using `rattler-build` invoked through pixi tasks).
- Change-detection (e.g. AST-based dep-graph analysis) still belongs upstream of the matrix — `pixi install` solves the whole workspace either way; you want CI to skip building unaffected packages from source.

## Gotchas encountered

| Gotcha | Workaround |
|---|---|
| **`[workspace.dependencies]` rejected on pixi 0.69**, even though the canonical `polyglot-particles` example in `prefix-dev/pixi/examples/pixi-build/polyglot-particles` uses it. `{ workspace = true }` in sub-packages fails the same way. | Inline pins on each sub-package (`python = "3.12.*"`, `maturin = ">=1.7,<2.0"`). Re-evaluate when pixi releases the next minor with `[workspace.dependencies]` support. |
| **Same-name `tests/` directories across sub-packages** collide under default pytest import mode (`ModuleNotFoundError: No module named 'tests.test_cli'`). | Add `--import-mode=importlib` to the pytest invocation and don't put `__init__.py` files in the `tests/` directories. |
| **Single-command Typer apps collapse to direct invocation**, so `cli-foo subcmd args` parses `subcmd` as the function's first positional argument. | Add an empty `@app.callback()` to force subcommand mode, or register a second `@app.command()`. |
| **`pixi self-update`** errors on a conda-installed pixi binary. | Install the latest pixi to `~/.pixi/bin` via the official `https://pixi.sh/install.sh` script. Add to PATH before the conda-managed copy. |

## Recommended migration order (for porting this into a real monorepo)

1. **One leaf pure-Python lib first**. Add a `pyproject.toml` with `[tool.pixi.package.*]`, verify `pixi-build-python` accepts it, confirm `pixi install` builds it.
2. **One PyO3 cdylib + its rust crates** as a group. Confirm the rust toolchain is provisioned via the backend and that path deps from the python side resolve.
3. **The full pattern: PyO3 cdylib + pure-Python wrapper + downstream app**. Confirm transitive closures and that `pixi install` solves them cleanly.
4. **Scale up to multiple groups** (i.e. a second rust group with its own cdylib). Confirm cross-group Python libs work.
5. **Decide one vs two Cargo workspaces** based on observed feature-graph behaviour. Default to one.
6. **App / docker / CI plumbing** last. The per-package conda artifacts produced under `.pixi/artifacts-v0/` are the unit of distribution.

## What this plan does **not** cover

- Cross-platform builds for any platform not in `workspace.platforms`. The trial built on linux-64 only; `osx-arm64` was declared and solves cleanly but wasn't actually compiled.
- Publishing to a public conda channel. The trial used local builds only.
- Migrating from an existing `[feature.X.dependencies]`-style pixi config to the `pixi-build` pattern — separate concern.
- IDE / language-server integration (rust-analyzer, ruff-lsp). Should work without special configuration but wasn't exercised.

## Pinned toolchain

For reproducibility:

- pixi ≥ 0.69 (preview feature `pixi-build`)
- `pixi-build-python` 0.4.*
- maturin ≥ 1.7, < 2.0
- pyo3 0.22
- python 3.12.*
- rust toolchain — provisioned by the backend; not pinned here. Pin in a future version of this plan if reproducibility across rust releases becomes a concern.
