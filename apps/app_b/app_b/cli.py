import numpy as np
import typer
from nm_b.some_func import func_b
from nm_c.libnm_c import fast_sum

app = typer.Typer()


@app.command()
def hello(name: str):
    a = np.array([1, 2, 3])
    typer.echo(f"Hello {name}, {fast_sum(a)=}. Calling func_b()")
    func_b()
