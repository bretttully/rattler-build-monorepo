# pixi-build monorepo trial

End-to-end trial of a [`pixi`](https://pixi.sh) + `pixi-build` monorepo combining pure-Rust crates, PyO3 cdylibs, pure-Python libraries, and Python apps under a single workspace. The structure mirrors patterns common in real-world rust/python monorepos: multi-crate "groups" wrapped by a single PyO3 binding, pure-Python downstreams that pull in subsets, and apps with divergent transitive closures.

## Layout

```
.
├── Cargo.toml                   # single Rust workspace
├── pixi.toml                    # pixi workspace; pixi-build (preview)
├── PIXI_PLAN.md                 # findings, recommended pattern, gotchas
├── rust/                        # pure-Rust crates, grouped by domain
│   ├── fastthing-core/          #   group "fastthing": base ops
│   ├── fastthing-stats/         #     depends on fastthing-core
│   ├── geocompute-core/         #   group "geocompute": geometry primitives
│   └── geocompute-tiles/        #     depends on geocompute-core
├── python/                      # PyO3 cdylibs (one per rust group)
│   ├── fastthing/               #   re-exports fastthing-core + fastthing-stats
│   └── geocompute/              #   re-exports geocompute-core + geocompute-tiles
├── libs/                        # pure-Python libs
│   ├── slowthing/               #   depends on `fastthing` only
│   └── geoanalysis/             #   depends on `fastthing` + `geocompute`
└── apps/                        # Python apps with different transitive closures
    ├── cli_simple/              #   slowthing  (math only)
    └── cli_full/                #   geoanalysis (math + geometry)
```

Each leaf package has its own `pyproject.toml` (or `Cargo.toml`) declaring its dependencies, and the root `pixi.toml` lists the two top-of-graph apps as workspace dependencies. The full graph is pulled in transitively from those entry points.

## Running

```bash
pixi install               # solves the workspace, builds all source packages
pixi run test              # runs every Python test suite
pixi run test-rust         # runs every Rust test suite
pixi run lint              # ruff format check + ruff check
pixi run demo-simple       # cli-simple summarise 1 2 3 4 5
pixi run demo-full         # cli-full tile-stats 0.5 0.5 1.0 1.0 5.0 5.0 ...
```

## What this validates

- **Multi-crate Rust groups**: `fastthing-{core,stats}` and `geocompute-{core,tiles}` — exactly the pattern of e.g. `tilemask-{core,catalogue,strtree}` in a real-world monorepo.
- **PyO3 cdylib re-exports across a group**: each `python/<lib>` exposes both crates of its group as a single Python module.
- **Mixed pure-Python and PyO3-backed deps**: `libs/slowthing` pulls one PyO3 group; `libs/geoanalysis` pulls two.
- **Divergent app dep graphs**: `cli_simple` doesn't pull in `geocompute` at all; `cli_full` pulls the full tree. Validates that pixi-build can prune correctly per-app.

See `PIXI_PLAN.md` for the verdict on `pixi-build` vs hybrid alternatives, the manifest patterns that worked, and any preview-feature gaps encountered.

## Preview feature status

`pixi-build` is a preview feature. This trial pins:

- pixi `>= 0.69`
- maturin `>= 1.7, < 2.0`
- pyo3 `0.22`
- python `3.12.*`
