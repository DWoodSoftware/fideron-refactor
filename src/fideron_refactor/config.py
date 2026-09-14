import json
from pathlib import Path

DEFAULT_CONFIG = {
    "version": 1,
    "profile": "default",
    "base_branch": "main",
    "ignore": [],
    "audit": {
        "history": True,
    },
    "branch_drift": {
        "max_changed_files": 20,
        "max_changed_lines": 800,
    },
}

REQUIRED_CONFIG_FIELDS = (
    "version",
    "profile",
    "base_branch",
    "audit",
    "branch_drift",
)

REQUIRED_NESTED_FIELDS = (
    ("audit", "history"),
    ("branch_drift", "max_changed_files"),
    ("branch_drift", "max_changed_lines"),
)


class ConfigError(Exception):
    pass


def load_config():
    config_path = Path.cwd() / "refactor.json"
    config = _read_config(config_path)

    _validate_required_fields(config)
    _validate_ignore(config)
    _reconcile_profile(config, config_path)

    return config

def _read_config(config_path: Path) -> dict:
    try:
        return json.loads(
            config_path.read_text(encoding="utf-8")
        )
    except FileNotFoundError as exc:
        raise ConfigError(
            "Refactor configuration not found"
        ) from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(
            "Invalid Refactor configuration"
        ) from exc

def _validate_required_fields(config: dict) -> None:
    for field in REQUIRED_CONFIG_FIELDS:
        if field not in config:
            raise ConfigError(
                f"Missing required configuration field: {field}"
            )

    for parent, field in REQUIRED_NESTED_FIELDS:
        if field not in config[parent]:
            raise ConfigError(
                "Missing required configuration field: "
                f"{parent}.{field}"
            )

def _validate_ignore(config: dict) -> None:
    config.setdefault("ignore", [])

    if not isinstance(config["ignore"], list) or not all(
        isinstance(path, str)
        for path in config["ignore"]
    ):
        raise ConfigError(
            "Invalid Refactor ignore configuration"
        )

def _reconcile_profile(
    config: dict,
    config_path: Path,
) -> None:
    if config.get("profile") != "default":
        return

    if _without_profile(config) == _without_profile(DEFAULT_CONFIG):
        return

    config["profile"] = "custom"

    config_path.write_text(
        json.dumps(config, indent=2),
        encoding="utf-8",
    )

def _without_profile(config: dict) -> dict:
    return {
        key: value
        for key, value in config.items()
        if key != "profile"
    }