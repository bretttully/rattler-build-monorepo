from typer.testing import CliRunner

from cli_full.__main__ import app

runner = CliRunner()


def test_tile_stats():
    result = runner.invoke(
        app,
        ["tile-stats", "0.5", "0.5", "1.0", "1.0", "5.0", "5.0", "--tile-max-x", "2", "--tile-max-y", "2"],
    )
    assert result.exit_code == 0
    assert "inside = 2" in result.stdout


def test_tile_stats_validation():
    result = runner.invoke(app, ["tile-stats", "0.5"])
    assert result.exit_code == 2
