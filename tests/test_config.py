import json

import pytest
from fideron_refactor.config import DEFAULT_CONFIG, ConfigError, load_config


def test_load_config_reads_repository_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    expected_config = {
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

    config_path = audits_dir / "config.json"
    config_path.write_text(
        json.dumps(expected_config),
        encoding="utf-8",
    )

    config = load_config()

    assert config == expected_config

def test_default_config_matches_repository_init_contract():
    assert DEFAULT_CONFIG == {
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

def test_load_config_marks_modified_default_profile_as_custom(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    modified_config = {
        "version": 1,
        "profile": "default",
        "base_branch": "develop",
        "audit": {
            "history": True,
        },
        "branch_drift": {
            "max_changed_files": 20,
            "max_changed_lines": 800,
        },
    }

    config_path = audits_dir / "config.json"
    config_path.write_text(
        json.dumps(modified_config),
        encoding="utf-8",
    )

    config = load_config()

    assert config["profile"] == "custom"

    persisted_config = json.loads(
        config_path.read_text(encoding="utf-8")
    )
    assert persisted_config["profile"] == "custom"

def test_load_config_raises_config_error_for_invalid_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    config_path = audits_dir / "config.json"
    config_path.write_text(
        '{"profile": "default"',
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="Invalid Refactor configuration"):
        load_config()

def test_load_config_raises_config_error_when_profile_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    config_path = audits_dir / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "version": 1,
                "base_branch": "main",
                "audit": {
                    "history": True,
                },
                "branch_drift": {
                    "max_changed_files": 20,
                    "max_changed_lines": 800,
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="Missing required configuration field: profile"):
        load_config()

def test_load_config_raises_config_error_when_version_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    config_path = audits_dir / "config.json"
    config_path.write_text(
        json.dumps(
            {
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
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigError,
        match="Missing required configuration field: version",
    ):
        load_config()

def test_load_config_raises_config_error_when_base_branch_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    config_path = audits_dir / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "version": 1,
                "profile": "default",
                "audit": {
                    "history": True,
                },
                "branch_drift": {
                    "max_changed_files": 20,
                    "max_changed_lines": 800,
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigError,
        match="Missing required configuration field: base_branch",
    ):
        load_config()

def test_load_config_raises_config_error_when_audit_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    config_path = audits_dir / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "version": 1,
                "profile": "default",
                "base_branch": "main",
                "branch_drift": {
                    "max_changed_files": 20,
                    "max_changed_lines": 800,
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigError,
        match="Missing required configuration field: audit",
    ):
        load_config()

def test_load_config_raises_config_error_when_branch_drift_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    config_path = audits_dir / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "version": 1,
                "profile": "default",
                "base_branch": "main",
                "audit": {
                    "history": True,
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigError,
        match="Missing required configuration field: branch_drift",
    ):
        load_config()

def test_load_config_raises_config_error_when_audit_history_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    config_path = audits_dir / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "version": 1,
                "profile": "default",
                "base_branch": "main",
                "audit": {},
                "branch_drift": {
                    "max_changed_files": 20,
                    "max_changed_lines": 800,
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigError,
        match="Missing required configuration field: audit.history",
    ):
        load_config()

def test_load_config_raises_config_error_when_max_changed_files_is_missing(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    config_path = audits_dir / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "version": 1,
                "profile": "default",
                "base_branch": "main",
                "audit": {
                    "history": True,
                },
                "branch_drift": {
                    "max_changed_lines": 800,
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigError,
        match="Missing required configuration field: branch_drift.max_changed_files",
    ):
        load_config()

def test_load_config_raises_config_error_when_max_changed_lines_is_missing(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    audits_dir = tmp_path / "audits"
    audits_dir.mkdir()

    config_path = audits_dir / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "version": 1,
                "profile": "default",
                "base_branch": "main",
                "audit": {
                    "history": True,
                },
                "branch_drift": {
                    "max_changed_files": 20,
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigError,
        match="Missing required configuration field: branch_drift.max_changed_lines",
    ):
        load_config()