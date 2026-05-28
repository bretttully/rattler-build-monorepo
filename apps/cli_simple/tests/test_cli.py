from typer.testing import CliRunner

from cli_simple.__main__ import app

runner = CliRunner()


def test_add():
    result = runner.invoke(app, ["add", "1", "2", "3", "4", "5"])
    assert result.exit_code == 0
    assert "15" in result.stdout


def test_describe():
    result = runner.invoke(app, ["describe", "7", "8"])
    assert result.exit_code == 0
    assert "7 + 8 = 15" in result.stdout


def test_summarise():
    result = runner.invoke(app, ["summarise", "1", "2", "3", "4", "5"])
    assert result.exit_code == 0
    assert "n = 5" in result.stdout
    assert "mean = 3" in result.stdout
