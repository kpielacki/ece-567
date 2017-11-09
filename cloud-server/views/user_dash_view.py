from flask_admin import expose
from flask_login import current_user
from init_dash import user_dash
from secure_views import SecureBaseView


class UserDashView(SecureBaseView):

    def is_visible(self):
        return current_user.is_authenticated

    def __init__(self, *args, **kwargs):
        self.app = kwargs.pop('app', True)
        SecureBaseView.__init__(self, *args, **kwargs)

    @expose('/')
    def index(self):
        scripts = self.app._generate_scripts_html()
        css = self.app._generate_css_dist_html()
        config = self.app._generate_config_html()
        return self.render('admin/dash_view.html', scripts=scripts, css=css,
                           dashconfig=config)
