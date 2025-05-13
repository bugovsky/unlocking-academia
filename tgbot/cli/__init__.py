import typer

from tgbot.cli.entrypoint import tgbot

app = typer.Typer(no_args_is_help=True)
app.add_typer(tgbot, name="run")


if __name__ == "__main__":
    app()
