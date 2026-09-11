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

def load_config():
    config_path = Path.cwd() / "audits" / "config.json"

    return json.loads(
        config_path.read_text(encoding="utf-8")
    )