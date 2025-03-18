from flask_admin import AdminIndexView, expose


class DashboardView(AdminIndexView):
    def is_visible(self):
        return False