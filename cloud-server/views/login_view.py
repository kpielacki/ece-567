import datetime
from flask import (request, url_for, redirect, flash, current_app)
from flask_admin import (BaseView, expose)
from flask_login import current_user


class LoginView(BaseView):

    def is_visible(self):
        return False

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        # TODO: Add redirect and post login method
        next = request.args.get("next")
        if current_user.is_authenticated:
            return redirect('/')
        
        return self.render('display.html', content='TEST LOGIN')

