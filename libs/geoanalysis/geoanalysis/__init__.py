"""Cross-domain aggregation: combines fastthing (stats) and geocompute (geometry).

Demonstrates a pure-Python lib that depends on two separate PyO3 cdylibs from
this monorepo, each themselves backed by a group of pure-Rust crates.
"""

from collections.abc import Iterable

import fastthing
import geocompute


Point = tuple[float, float]


def tile_stats(
    points: Iterable[Point],
    tile_min: Point,
    tile_max: Point,
    reference: Point,
) -> dict:
    """For points inside the given tile, return count + mean distance from a reference + nearest point.

    Distances are scaled to micrometres before being passed to fastthing's int-based mean,
    illustrating data crossing two PyO3 cdylibs.
    """
    pts = list(points)
    inside = [p for p in pts if geocompute.point_in_tile(p, tile_min, tile_max)]
    if not inside:
        return {"inside": 0, "mean_distance": None, "nearest": None}
    distances_um = [int(round(geocompute.distance(reference, p) * 1_000_000)) for p in inside]
    return {
        "inside": len(inside),
        "mean_distance": fastthing.mean(distances_um) / 1_000_000 if fastthing.mean(distances_um) is not None else None,
        "nearest": geocompute.nearest_point(reference, inside),
    }
