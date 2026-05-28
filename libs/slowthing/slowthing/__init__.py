"""Pure-Python wrapper around the `fastthing` PyO3 extension.

Demonstrates that a pure-Python package in this monorepo can depend on a
PyO3 cdylib built from a sibling source package.
"""

from collections.abc import Iterable

import fastthing


def add_and_describe(a: int, b: int) -> str:
    """Add two integers via the Rust extension and return a human-readable string."""
    return f"{a} + {b} = {fastthing.add(a, b)}"


def sum_iterable(xs: Iterable[int]) -> int:
    """Sum any iterable of ints by materialising to a list and delegating to Rust."""
    return fastthing.sum_list(list(xs))


def summarise(xs: Iterable[int]) -> dict:
    """Compute n / sum / mean / variance for the iterable, all via the Rust extension."""
    materialised = list(xs)
    return {
        "n": len(materialised),
        "sum": fastthing.sum_list(materialised),
        "mean": fastthing.mean(materialised),
        "variance": fastthing.variance(materialised),
    }
