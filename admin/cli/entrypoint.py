import typer
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from backend.db.base import db_settings
from backend.db.models import User, Post, Comment

admin_app = typer.Typer(short_help="Запуск backend-приложения")


@admin_app.command(name="manage", short_help="Запустить админку")
def launch_admin():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123456790"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_settings.sync_url
    app.config["SQLALCHEMY_ECHO"] = True
    db = SQLAlchemy(app)

    admin = Admin(app, name="Unlocking Academia")
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Comment, db.session))
    app.run()
