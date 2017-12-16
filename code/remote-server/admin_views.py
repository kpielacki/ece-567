from admin_app_config import db
from models import (User, HazardSummary, HazardLocation)
from views.home_view import HomeView
from views.login_view import LoginView
from views.logout_view import LogoutView
from views.user_view import UserView
from views.mobile_view import (MobileLoginView, MobileView)
from views.user_dash_view import UserDashView
from views.business_dash_view import BusinessDashView
from views.hazard_summary_view import HazardSummaryView
from views.hazard_location_view import HazardLocationView


def add_admin_views(admin, app):
    # Home View
    admin.add_view(HomeView(name='Home', endpoint='home'))

    # Mobile view handling
    admin.add_view(MobileLoginView(
        name='Mobile Login', endpoint='mobilelogin'))
    admin.add_view(MobileView(name='Mobile', endpoint='mobile'))

    # User dash view handling
    admin.add_view(UserDashView(name='User Portal', endpoint='userdash',
                   app=app))
    admin.add_view(BusinessDashView(name='Business Portal',
                                    endpoint='businessdash', app=app))

    # Admin portal views
    admin.add_view(UserView(User, db.session, name='Users'))
    admin.add_view(HazardSummaryView(
        HazardSummary, db.session, name='Hazard Summary'))
    admin.add_view(HazardLocationView(
        HazardLocation, db.session, name='Hazard Locations'))

    # Login and Logout views
    admin.add_view(LoginView(name='Login', endpoint='login'))
    admin.add_view(LogoutView(name='Logout', endpoint='logout'))
