from admin_app_config import db
import datetime
from flask import (abort, Response, request, url_for, redirect, flash,
                   current_app)
from flask_admin import (BaseView, expose)
from flask_login import current_user
from werkzeug.security import (generate_password_hash, check_password_hash)
from models import User
import json


class MobileView(BaseView):

    def is_visible(self):
        return False

    def handle_request(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None or password is None: return (400, 'Bad Request')
        user_info = User.query.filter_by(email=email).first()

        # Handle registration
        if user_info is not None:
            if check_password_hash(user_info.password, password):
                return (200, 'Login Successful')
            else: return (400, 'Invalid Username or Password')

        # Check password
        pw_hash = generate_password_hash(password)
        try:
            new_user = User(email=email, password=pw_hash)
            db.session.add(new_user)
            db.session.commit()
        except:
            return (500, 'Server Error')
        return (200, 'Registered New Account')

    @expose('/', methods=('POST',))
    def index(self):
        if request.method == 'POST':
            try:
                request_dict = json.loads(request.data)
            except Exception as e:
                return abort(400)

            code, msg = self.handle_request(request_dict)
            return Response(msg, status=code, mimetype='text/plain')
        else:
            return abort(400)
