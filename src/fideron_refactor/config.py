import json
from pathlib import Path


def load_config():
    config_path = Path.cwd() / "audits" / "config.json"

    return json.loads(
        config_path.read_text(encoding="utf-8")
    )