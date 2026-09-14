import json
from pathlib import Path
from typing import Annotated

import typer

from fideron_refactor.audit import audit_repository
from fideron_refactor.config import load_config
from fideron_refactor.findings import is_cleanup_target
from fideron_refactor.init import initialise_repo

app = typer.Typer(
    help="Fideron repository refactoring and audit CLI",
    invoke_without_command=True,
)

@app.callback()
def root(
    init: Annotated[
        bool,
        typer.Option(
            "--init",
            help="Initialise Refactor for the current repository.",
        ),
    ] = False,
    ignore: Annotated[
        list[str] | None,
        typer.Option(
            "--ignore",
            help="Add a repository-relative path to the audit ignore list.",
        ),
    ] = None,
    base: Annotated[
        str | None,
        typer.Option(
            "--base",
            help="Base branch used for repository comparison.",
        ),
    ] = None,
    max_diff_files: Annotated[
        int | None,
        typer.Option(
            "--max-diff-files",
            min=1,
            help=(
                "Maximum changed files before branch drift "
                "is flagged."
            ),
        ),
    ] = None,
    max_diff_lines: Annotated[
        int | None,
        typer.Option(
            "--max-diff-lines",
            min=1,
            help=(
                "Maximum changed lines before branch drift "
                "is flagged."
            ),
        ),
    ] = None,
):
    if init:
        custom_profile = any(
            value is not None
            for value in (
                base,
                max_diff_files,
                max_diff_lines,
            )
        ) or bool(ignore)

        initialise_repo(
            base_branch=base or "main",
            max_diff_files=max_diff_files or 20,
            max_diff_lines=max_diff_lines or 800,
            profile="custom" if custom_profile else "default",
        )

    if ignore:
        for ignore_path in ignore:
            add_ignore_path(ignore_path)

@app.command()
def cleanup():
    findings = audit_repository()

    cleanup_targets = [
        finding
        for finding in findings
        if is_cleanup_target(finding)
    ]

    for finding in cleanup_targets:
        typer.echo(
            f"CLEANUP: {finding['value']} - {finding['reason']}"
        )

def add_ignore_path(ignore_path: str) -> None:
    config = load_config()

    normalised_path = (
        ignore_path
        .replace("\\", "/")
        .removeprefix("./")
        .rstrip("/")
    )

    if normalised_path not in config["ignore"]:
        config["ignore"].append(normalised_path)

    config["profile"] = "custom"

    config_path = Path.cwd() / "refactor.json"
    config_path.write_text(
        json.dumps(config, indent=2),
        encoding="utf-8",
    )

def main():
    app()


if __name__ == "__main__":
    main()