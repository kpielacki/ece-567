from admin_app_config import db
from models import User
from views.login_view import LoginView
from views.user_view import UserView
from views.mobile_view import MobileView
from views.user_dash_view import UserDashView


def add_admin_views(admin, app):
    # Login view
    admin.add_view(LoginView(name='Login', endpoint='login'))

    # Test user view
    admin.add_view(UserView(User, db.session, name='Users'))

    # Mobile view handling
    admin.add_view(MobileView(name='mobile', endpoint='mobile'))
    
    # User dash view handling
    admin.add_view(UserDashView(name='userdash', endpoint='userdash', app=app))
