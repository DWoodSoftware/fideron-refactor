import json

from fideron_refactor.config import load_config


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