from pathlib import Path


def initialise_repo():
    audits_dir = Path.cwd() / "audits"
    audits_dir.mkdir(exist_ok=True)

    config_path = audits_dir / "config.json"
    config_path.touch(exist_ok=True)