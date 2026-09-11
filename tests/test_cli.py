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
    assert (tmp_path / "audits" / "history").is_dir()

def test_init_does_not_overwrite_existing_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    config_path = audits_dir / "config.json"
    existing_config = '{"profile": "custom"}'
    config_path.write_text(existing_config, encoding="utf-8")

    result = runner.invoke(app, ["--init"])

    assert result.exit_code == 0
    assert config_path.read_text(encoding="utf-8") == existing_config

def test_init_with_custom_arguments_writes_custom_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        [
            "--init",
            "--base",
            "develop",
            "--max-diff-files",
            "30",
            "--max-diff-lines",
            "1500",
        ],
    )

    assert result.exit_code == 0

    config_path = tmp_path / "audits" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    assert config == {
        "version": 1,
        "profile": "custom",
        "base_branch": "develop",
        "audit": {
            "history": True,
        },
        "branch_drift": {
            "max_changed_files": 30,
            "max_changed_lines": 1500,
        },
    }

def test_init_with_explicit_default_values_marks_profile_custom(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        [
            "--init",
            "--base",
            "main",
            "--max-diff-files",
            "20",
            "--max-diff-lines",
            "800",
        ],
    )

    assert result.exit_code == 0

    config_path = tmp_path / "audits" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    assert config["profile"] == "custom"