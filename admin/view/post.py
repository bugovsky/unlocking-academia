import datetime

from flask_admin.contrib.sqla import ModelView
from wtforms.fields.choices import SelectMultipleField

from backend.schema.base import Domain


class PostModelView(ModelView):
    form_excluded_columns = ["views", "comments", "ratings", "created_at", "updated_at", "deleted_at"]
    column_list = ["content", "media_urls", "domain", "id"]
    column_labels = {
        "content": "Текст поста",
        "media_urls": "Медиа-контент",
        "domain": "Академические дисциплины",
    }
    form_overrides = {
        'domain': SelectMultipleField
    }
    form_args = {
        'domain': {
            'choices': [(d.value, d.value) for d in Domain],
            'coerce': str,
        }
    }

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.views = 0
            model.created_at = datetime.datetime.now()
            model.updated_at = datetime.datetime.now()
            model.deleted_at = None

        super().on_model_change(form, model, is_created)