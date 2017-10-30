from flask import render_template
from flask_admin import (BaseView, expose)


class HomeView(BaseView):

    @expose('/')
    def index(self):
        return render_template('home.html')
