from flask_admin import (BaseView, expose)
from init_dash import user_dash


class UserDashView(BaseView):

    def __init__(self, *args, **kwargs):
        self.app = kwargs.pop('app', True)
        BaseView.__init__(self, *args, **kwargs)

    @expose('/')
    def index(self):
        scripts = self.app._generate_scripts_html()
        css = self.app._generate_css_dist_html()
        config = self.app._generate_config_html()
        return self.render('admin/dash_view.html', scripts=scripts, css=css,
                           dashconfig=config)
