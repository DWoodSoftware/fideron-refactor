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

    config = json.loads(
        config_path.read_text(encoding="utf-8")
    )

    if config.get("profile") == "default":
        comparible_config = {
            key: value
            for key, value in config.items()
            if key != "profile"
        }

        comparible_default = {
            key: value
            for key, value in DEFAULT_CONFIG.items()
            if key != "profile"
        }

        if comparible_config != comparible_default:
            config["profile"] = "custom"

            config_path.write_text(
                json.dumps(config, indent=2),
                encoding="utf-8",
            )

    return config