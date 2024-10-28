import typer
from nm_a.some_func import func_a

app = typer.Typer()


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}. Calling func_a()")
    func_a()
