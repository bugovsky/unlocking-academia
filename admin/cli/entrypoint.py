import typer
from flask_sqlalchemy import SQLAlchemy


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from admin.bot import TgBotContent
from admin.wsgi import app
from backend.db.models import User, Post, Comment

admin_app = typer.Typer(short_help="Запуск backend-приложения")


@admin_app.command(name="manage", short_help="Запустить админку")
def launch_admin():
    db = SQLAlchemy(app)

    admin = Admin(app, name="Unlocking Academia")
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(TgBotContent(name='Content', endpoint='content'))
    app.run()
