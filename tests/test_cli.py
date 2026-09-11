import json

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

    config_path = tmp_path / "audits" / "config.json"

    assert result.exit_code == 0
    assert (tmp_path / "audits").is_dir()
    assert config_path.is_file()

    config = json.loads(config_path.read_text(encoding="utf-8"))

    assert config == {
        "version": 1,
        "profile": "default",
        "base_branch": "main",
        "audit": {
            "history": True,
        },
        "branch_drift": {
            "max_changed_files": 20,
            "max_changed_lines": 800,
        },
    }