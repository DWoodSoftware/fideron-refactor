from pathlib import Path

import typer

from fideron_refactor.init import initialise_repo

app = typer.Typer(
    help="Fideron repository refactoring and audit CLI",
    invoke_without_command=True,
)

@app.callback()
def root(
    init: bool = typer.Option(
        False,
        "--init",
        help="Initialise Refactor for the current repository.",
    ),
    base: str | None = typer.Option(
        None,
        "--base",
        help="Base branch used for repository comparison.",
    ),
    max_diff_files: int | None = typer.Option(
        None,
        "--max-diff-files",
        min=1,
        help="Maximum changed files before branch drift is flagged.",
    ),
    max_diff_lines: int | None = typer.Option(
        None,
        "--max-diff-lines",
        min=1,
        help="Maximum changed lines before branch drift is flagged.",
    ),
):
    if init:
        custom_profile = any(
            value is not None
            for value in (
                base,
                max_diff_files,
                max_diff_lines,
            )
        )

        initialise_repo(
            base_branch=base or "main",
            max_diff_files=max_diff_files or 20,
            max_diff_lines=max_diff_lines or 800,
            profile="custom" if custom_profile else "default",
        )


def main():
    app()


if __name__ == "__main__":
    main()