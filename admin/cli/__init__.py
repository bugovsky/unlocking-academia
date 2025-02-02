import typer

from admin.cli.entrypoint import admin_app

app = typer.Typer(no_args_is_help=True)
app.add_typer(admin_app, name="run")


if __name__ == "__main__":
    app()
