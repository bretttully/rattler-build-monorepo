from app_b.cli import app
from typer.testing import CliRunner


def test_hello():
    runner = CliRunner()
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert result.stdout == "Hello hello. Calling func_b()\nfunc_a() in nm_a\n"
