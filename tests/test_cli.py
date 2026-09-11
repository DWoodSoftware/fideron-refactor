from fideron_refactor.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_cli_help_is_available():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Fideron repository refactoring and audit CLI" in result.stdout

def test_init_creates_default_audit_scaffold(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["--init"])

    assert result.exit_code == 0
    assert (tmp_path / "audits").is_dir()
    assert (tmp_path / "audits" / "config.json").is_file()