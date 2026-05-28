"""Full pipeline demo CLI: geometry + stats combined.

Pulls in geoanalysis -> {fastthing, geocompute} PyO3 extensions
-> {fastthing-core, fastthing-stats, geocompute-core, geocompute-tiles}.
Demonstrates the largest transitive closure in the workspace.
"""

import typer

import geoanalysis

app = typer.Typer(help=__doc__)


@app.callback()
def main() -> None:
    """Full pipeline demo CLI."""


@app.command()
def tile_stats(
    points: list[float] = typer.Argument(..., help="Flat list of point coords: x1 y1 x2 y2 ..."),
    tile_min_x: float = typer.Option(0.0),
    tile_min_y: float = typer.Option(0.0),
    tile_max_x: float = typer.Option(10.0),
    tile_max_y: float = typer.Option(10.0),
    ref_x: float = typer.Option(0.0),
    ref_y: float = typer.Option(0.0),
) -> None:
    """Compute tile-bounded stats for a list of points."""
    if len(points) % 2 != 0:
        typer.echo("Error: points must be a flat list of pairs (even number of values)", err=True)
        raise typer.Exit(code=2)
    pairs = [(points[i], points[i + 1]) for i in range(0, len(points), 2)]
    out = geoanalysis.tile_stats(
        points=pairs,
        tile_min=(tile_min_x, tile_min_y),
        tile_max=(tile_max_x, tile_max_y),
        reference=(ref_x, ref_y),
    )
    for k, v in out.items():
        typer.echo(f"{k} = {v}")


if __name__ == "__main__":
    app()
