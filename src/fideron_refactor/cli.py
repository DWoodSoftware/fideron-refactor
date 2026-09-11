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
    )
):
    if init:
        initialise_repo()


def main():
    app()


if __name__ == "__main__":
    main()