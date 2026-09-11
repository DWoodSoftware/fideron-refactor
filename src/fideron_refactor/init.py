import json
from pathlib import Path

DEFAULT_CONFIG = {
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

def initialise_repo():
    audits_dir = Path.cwd() / "audits"
    audits_dir.mkdir(exist_ok=True)

    config_path = audits_dir / "config.json"
    config_path.write_text(
        json.dumps(DEFAULT_CONFIG, indent=2),
        encoding="utf-8",
    )