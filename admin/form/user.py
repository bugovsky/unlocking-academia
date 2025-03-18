from flask_admin.form import BaseForm
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.simple import StringField
from wtforms.widgets.core import ListWidget, CheckboxInput

from backend.schema.base import Domain


class UserForm(BaseForm):
    firstname = StringField("Имя")
    lastname = StringField("Фамилия")
    email = StringField("Почта")
    domain = SelectMultipleField(
        "Академические дисциплины",
        choices=[(d.value, d.value) for d in Domain],
        coerce=str,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
        render_kw={"class": "checkbox-list", "style": "list-style-type: none; padding-left: 0;"}
    )