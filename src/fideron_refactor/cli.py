import typer

app = typer.Typer(
    help="Fideron repository refactoring and audit CLI"
)


@app.callback()
def root():
    pass


def main():
    app()


if __name__ == "__main__":
    main()