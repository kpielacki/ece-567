from admin_app_config import db
from models import (User, HazardLocation)
from views.home_view import HomeView
from views.login_view import LoginView
from views.user_view import UserView
from views.mobile_view import MobileView
from views.user_dash_view import UserDashView
from views.hazard_location_view import HazardLocationView


def add_admin_views(admin, app):
    # Home View
    admin.add_view(HomeView(name='Home', endpoint='home'))
    # Mobile view handling
    admin.add_view(MobileView(name='Mobile', endpoint='mobile'))
    # User dash view handling
    admin.add_view(UserDashView(name='User Portal', endpoint='userdash', app=app))

    # Admin Portal Views
    admin.add_view(UserView(User, db.session, category='Admin', name='Users'))
    admin.add_view(HazardLocationView(
        HazardLocation, db.session, category='Admin', name='Hazard Locations'))

    # Login view
    admin.add_view(LoginView(name='Login', endpoint='login'))
