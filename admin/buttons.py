from flask import request, redirect, url_for, flash
from flask_admin import BaseView, expose

from common.manager import content_manager, KEYBOARD_INFO


class TgBotButtonsView(BaseView):
    @expose('/')
    def index(self):
        keyboards = [
            {
                "key": key,
                "name": info.name,
                "context": info.context,
                "buttons": content_manager.get_buttons(key)
            }
            for key, info in KEYBOARD_INFO.items()
        ]
        return self.render('admin/buttons.html', keyboards=keyboards)

    @expose('/edit/<key>', methods=['GET', 'POST'])
    def edit(self, key):
        if key not in KEYBOARD_INFO:
            flash(f"Клавиатура '{key}' не найдена.", 'error')
            return redirect(url_for('.index'))

        if request.method == 'POST':
            try:
                button_texts = request.form.getlist('button_text[]')
                button_urls = request.form.getlist('button_url[]')

                # Проверка на пустой список кнопок
                if not button_texts:
                    flash("Необходимо добавить хотя бы одну кнопку.", 'error')
                    return redirect(url_for('.edit', key=key))

                # Формируем список кнопок
                buttons = []
                for text, url in zip(button_texts, button_urls):
                    if not text.strip():
                        flash("Текст кнопки не может быть пустым.", 'error')
                        return redirect(url_for('.edit', key=key))
                    buttons.append({
                        "text": text.strip(),
                        "url": url.strip() if url.strip() else None
                    })

                content_manager.set_buttons(key, buttons)
                flash(f"Кнопки для '{KEYBOARD_INFO[key].name}' обновлены.", 'success')
                return redirect(url_for('.index'))
            except Exception as e:
                flash(f"Ошибка при сохранении кнопок: {str(e)}.", 'error')
                return redirect(url_for('.edit', key=key))

        buttons = content_manager.get_buttons(key)
        name = KEYBOARD_INFO[key].name
        context = KEYBOARD_INFO[key].context
        return self.render('admin/buttons_edit.html', key=key, name=name, context=context, buttons=buttons)