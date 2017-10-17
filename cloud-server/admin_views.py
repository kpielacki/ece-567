from admin_app_config import db
from models import User
from views.login_view import LoginView
from views.user_view import UserView


def add_admin_views(admin):
    # Login view
    admin.add_view(LoginView(name='Login', endpoint='login'))

    # Test user view
    admin.add_view(UserView(User, db.session, name='Users'))
