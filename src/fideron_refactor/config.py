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

class ConfigError(Exception):
    pass

def load_config():
    config_path = Path.cwd() / "audits" / "config.json"

    try:
        config = json.loads(
            config_path.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        raise ConfigError(
            "Invalid Refactor configuration"
        ) from exc

    if "version" not in config:
        raise ConfigError(
            "Missing required configuration field: version"
        )

    if "profile" not in config:
        raise ConfigError(
            "Missing required configuration field: profile"
        )

    if "base_branch" not in config:
        raise ConfigError(
            "Missing required configuration field: base_branch"
        )

    if "audit" not in config:
        raise ConfigError(
            "Missing required configuration field: audit"
        )

    if "branch_drift" not in config:
        raise ConfigError(
            "Missing required configuration field: branch_drift"
        )

    if "history" not in config["audit"]:
        raise ConfigError(
            "Missing required configuration field: audit.history"
        )

    if "max_changed_files" not in config["branch_drift"]:
        raise ConfigError(
            "Missing required configuration field: branch_drift.max_changed_files"
        )

    if "max_changed_lines" not in config["branch_drift"]:
        raise ConfigError(
            "Missing required configuration field: branch_drift.max_changed_lines"
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