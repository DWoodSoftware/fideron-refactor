import json
from pathlib import Path

DEFAULT_BASE_BRANCH = "main"
DEFAULT_MAX_DIFF_FILES = 20
DEFAULT_MAX_DIFF_LINES = 800

def initialise_repo(
    base_branch=DEFAULT_BASE_BRANCH,
    max_diff_files=DEFAULT_MAX_DIFF_FILES,
    max_diff_lines=DEFAULT_MAX_DIFF_LINES,
    profile="default",
):
    audits_dir = Path.cwd() / "audits"
    audits_dir.mkdir(exist_ok=True)

    config_path = audits_dir / "config.json"

    if config_path.exists():
        return

    config = {
        "version": 1,
        "profile": profile,
        "base_branch": base_branch,
        "audit": {
            "history": True,
        },
        "branch_drift": {
            "max_changed_files": max_diff_files,
            "max_changed_lines": max_diff_lines,
        },
    }
    
    config_path.write_text(
        json.dumps(config, indent=2),
        encoding="utf-8",
    )