import json

from typer.testing import CliRunner

from fideron_refactor.cli import app
from fideron_refactor.findings import is_cleanup_target

runner = CliRunner()


def test_cli_help_is_available():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Fideron repository refactoring and audit CLI" in result.stdout

def test_init_creates_default_audit_scaffold(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    config_path = audits_dir / "config.json"
    existing_config = '{"profile": "custom"}'
    config_path.write_text(existing_config, encoding="utf-8")

    result = runner.invoke(app, ["--init"])

    assert result.exit_code == 0
    assert config_path.read_text(encoding="utf-8") == existing_config
    assert "Refactor is already initialised for this repository." in result.stdout

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

def test_init_rejects_zero_max_diff_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        [
            "--init",
            "--max-diff-files",
            "0",
        ],
    )

    assert result.exit_code != 0
    assert not (tmp_path / "audits" / "config.json").exists()

def test_init_rejects_zero_max_diff_lines(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        [
            "--init",
            "--max-diff-lines",
            "0",
        ],
    )

    assert result.exit_code != 0
    assert not (tmp_path / "audits" / "config.json").exists()

def test_init_rejects_negative_diff_threshold(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        [
            "--init",
            "--max-diff-files",
            "-1",
        ],
    )

    assert result.exit_code != 0
    assert not (tmp_path / "audits" / "config.json").exists()

def test_cleanup_reports_repository_cleanup_findings(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    source_file = tmp_path / "example.py"
    source_file.write_text(
        'API_URL = "http://localhost:8080"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.discover_repository_files",
        lambda: ["example.py"],
    )

    result = runner.invoke(app, ["cleanup"])

    assert result.exit_code == 0
    assert "CLEANUP" in result.stdout
    assert "localhost" in result.stdout.lower()

def test_secret_finding_is_cleanup_target():
    finding = {
        "category": "SECRET",
        "value": "api_key = abc123",
        "reason": "Possible secret",
    }

    assert is_cleanup_target(finding) is True

def test_extract_finding_is_cleanup_target():
    finding = {
        "category": "EXTRACT",
        "value": "scheduler.json",
        "reason": "Hardcoded configuration",
    }

    assert is_cleanup_target(finding) is True


def test_review_finding_is_not_cleanup_target():
    finding = {
        "category": "REVIEW",
        "value": "possible refactor",
        "reason": "Needs review",
    }

    assert is_cleanup_target(finding) is False


def test_keep_finding_is_not_cleanup_target():
    finding = {
        "category": "KEEP",
        "value": "intentional constant",
        "reason": "Expected repository value",
    }

    assert is_cleanup_target(finding) is False

def test_init_adds_audits_directory_to_gitignore(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["--init"])

    assert result.exit_code == 0

    gitignore = tmp_path / ".gitignore"

    assert gitignore.exists()
    assert "/audits/" in gitignore.read_text(encoding="utf-8")

def test_init_preserves_existing_gitignore_and_adds_audits_directory(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    gitignore = tmp_path / ".gitignore"
    gitignore.write_text(
        ".venv/\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["--init"])

    assert result.exit_code == 0

    contents = gitignore.read_text(encoding="utf-8")

    assert ".venv/" in contents
    assert "/audits/" in contents

def test_init_does_not_duplicate_audits_gitignore_entry(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    gitignore = tmp_path / ".gitignore"
    gitignore.write_text(
        "/audits/\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["--init"])

    assert result.exit_code == 0

    contents = gitignore.read_text(encoding="utf-8")

    assert contents.splitlines().count("/audits/") == 1