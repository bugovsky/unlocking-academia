from flask import Flask

from admin.config import admin_settings


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = admin_settings.secret_key

    app.config["SQLALCHEMY_DATABASE_URI"] = admin_settings.db_url
    app.config["SQLALCHEMY_ECHO"] = admin_settings.db_echo

    return app

app = create_app()