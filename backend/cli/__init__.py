import typer

from backend.cli.entrypoint import backend_app

app = typer.Typer(no_args_is_help=True)
app.add_typer(backend_app, name="run")


if __name__ == "__main__":
    app()
