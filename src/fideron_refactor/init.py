import json
from pathlib import Path

import typer

from fideron_refactor.config import DEFAULT_CONFIG


def ensure_gitignore_entry(directory: str) -> None:
    gitignore = Path.cwd() / ".gitignore"
    entry = f"/{directory.strip('/')}/"

    if gitignore.exists():
        contents = gitignore.read_text(encoding="utf-8")

        if entry in contents.splitlines():
            return

        if contents and not contents.endswith("\n"):
            contents += "\n"

        gitignore.write_text(
            contents + entry + "\n",
            encoding="utf-8",
        )
        return

    gitignore.write_text(
        entry + "\n",
        encoding="utf-8",
    )

def initialise_repo(
    base_branch=DEFAULT_CONFIG["base_branch"],
    max_diff_files=DEFAULT_CONFIG["branch_drift"]["max_changed_files"],
    max_diff_lines=DEFAULT_CONFIG["branch_drift"]["max_changed_lines"],
    profile=DEFAULT_CONFIG["profile"],
):
    audits_dir = Path.cwd() / "audits"
    audits_dir.mkdir(exist_ok=True)

    history_dir = audits_dir / "history"
    history_dir.mkdir(exist_ok=True)

    config_path = audits_dir / "config.json"

    ensure_gitignore_entry("audits")

    if config_path.exists():
        typer.echo("Refactor is already initialised for this repository.")
        return

    config = {
        "version": DEFAULT_CONFIG["version"],
        "profile": profile,
        "base_branch": base_branch,
        "audit": {
            "history": DEFAULT_CONFIG["audit"]["history"],
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