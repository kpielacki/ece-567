from flask import redirect, flash
from flask_login import logout_user, current_user
from flask_admin import BaseView, expose


class LogoutView(BaseView):

    def is_visible(self):
        return current_user.is_authenticated

    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            logout_user()
            flash("Logged Out Successfully")
        return redirect('/home')
