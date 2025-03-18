import secrets
import string

from flask_admin.contrib.sqla import ModelView

from admin.form.user import UserForm
from backend.schema.user import Role
from backend.utils.security import get_password_hash


class UserModelView(ModelView):
    form = UserForm

    def on_model_change(self, form, model, is_created):
        def _generate_password(length=12):
            alphabet = string.ascii_letters + string.digits + string.punctuation
            password = "".join(secrets.choice(alphabet) for _ in range(length))
            return password

        if is_created:
            raw_password = _generate_password()
            model.password = get_password_hash(raw_password)
            model.role = Role.EXPERT

        super().on_model_change(form, model, is_created)

    form_excluded_columns = ["password", "comments", "ratings", "requests", "responses", "created_at"]
    column_list = ("firstname", "lastname", "email", "domain")