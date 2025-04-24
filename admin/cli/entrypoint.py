import typer
from flask_sqlalchemy import SQLAlchemy


from flask_admin import Admin

from admin.buttons import TgBotButtonsView
from admin.content import TgBotContentView
from admin.view.comment import CommentModelView
from admin.view.home import DashboardView
from admin.view.post import PostModelView
from admin.view.user import UserModelView
from admin.wsgi import app
from backend.db.models import User, Post, Comment

admin_app = typer.Typer(short_help="Запуск backend-приложения")


@admin_app.command(name="manage", short_help="Запустить админку")
def launch_admin():
    db = SQLAlchemy(app)

    admin = Admin(app, name="Unlocking Academia - Admin Panel", index_view=DashboardView())
    admin.add_view(UserModelView(User, db.session, name="Пользователи"))
    admin.add_view(PostModelView(Post, db.session, name="Посты"))
    admin.add_view(CommentModelView(Comment, db.session, name="Комментарии"))
    admin.add_view(TgBotContentView(name="Содержимое ТГ-бота", endpoint="content"))
    admin.add_view(TgBotButtonsView(name="Кнопки ТГ-бота", endpoint="buttons"))
    app.run()
