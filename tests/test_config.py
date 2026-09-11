import json

from fideron_refactor.config import DEFAULT_CONFIG, load_config


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