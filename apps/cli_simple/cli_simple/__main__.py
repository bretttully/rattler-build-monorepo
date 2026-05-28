"""Math-only demo CLI: sums, describes, and summarises integer inputs.

Pulls in slowthing -> fastthing PyO3 extension -> fastthing-core + fastthing-stats.
Does NOT depend on geocompute, demonstrating divergent transitive closures across apps.
"""

import typer

import slowthing

app = typer.Typer(help=__doc__)


@app.callback()
def main() -> None:
    """Math-only demo CLI."""


@app.command()
def add(xs: list[int]) -> None:
    """Sum a list of integers (via the fastthing PyO3 extension)."""
    typer.echo(f"sum({xs}) = {slowthing.sum_iterable(xs)}")


@app.command()
def describe(a: int, b: int) -> None:
    """Add two integers and describe the result."""
    typer.echo(slowthing.add_and_describe(a, b))


@app.command()
def summarise(xs: list[int]) -> None:
    """Compute count, sum, mean, and variance of a list."""
    out = slowthing.summarise(xs)
    for k, v in out.items():
        typer.echo(f"{k} = {v}")


if __name__ == "__main__":
    app()
