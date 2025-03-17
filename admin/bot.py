from flask import request, redirect, url_for, flash
from flask_admin import BaseView, expose

from common.manager import content_manager, CONTENT_INFO


class TgBotContent(BaseView):
    @expose('/')
    def index(self):
        content = content_manager.get_all()
        display_content = [
            {"key": key, "name": CONTENT_INFO[key].name, "context": CONTENT_INFO[key].context, "value": value}
            for key, value in content.items()
        ]
        return self.render('admin/content.html', content=display_content)

    @expose('/edit/<key>', methods=['GET', 'POST'])
    def edit(self, key):
        content = content_manager.get_all()
        if key not in content:
            flash(f"Key '{key}' not found.", 'error')
            return redirect(url_for('.index'))

        if request.method == 'POST':
            new_value = request.form.get('value')
            if new_value is not None:
                content_manager.set(key, new_value)
                flash(f"Updated content for '{CONTENT_INFO[key].name}'.", 'success')
                return redirect(url_for('.index'))

        value = content_manager.get(key)
        name = CONTENT_INFO[key].name
        context = CONTENT_INFO[key].context
        return self.render('admin/content_edit.html', key=key, name=name, context=context, value=value)