import datetime

from flask_admin.contrib.sqla import ModelView
from wtforms.fields.choices import SelectMultipleField

from backend.schema.base import Domain


class CommentModelView(ModelView):
    column_list = ("content", "post_id")
    form_columns = ("content",)
    column_labels = {
        "content": "Комментарий",
        "post_id": "Идентификатор поста",
    }

    can_create = False