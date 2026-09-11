from fideron_refactor.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_cli_help_is_available():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Fideron repository refactoring and audit CLI" in result.stdout