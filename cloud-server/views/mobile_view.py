from admin_app_config import db
import datetime
from flask import (abort, Response, request, url_for, redirect, flash,
                   current_app)
from flask_admin import (BaseView, expose)
from flask_login import current_user
import json
import pandas as pd
from io import StringIO
from models import User
from werkzeug.security import (generate_password_hash, check_password_hash)


class MobileView(BaseView):

    def is_visible(self):
        return False

    def handle_login_request(self, data):
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

    def handle_json(self, data):
        try:
            return json.loads(request.data)
        except Exception as e:
            return None

    @expose('/', methods=('GET',))
    def index(self):
        return Response('<b>TEST MOBILE</b>', status=200, mimetype='text/html')

    @expose('/login/', methods=('POST',))
    def login(self):
        if request.method == 'POST':
            login_data = self.handle_json(request.data)
            if data_dict is None: return abort(400)
            code, msg = self.handle_login_request(login_data)
            return Response(msg, status=code, mimetype='text/plain')
        
        return abort(400)

    @expose('/echo/', methods=('POST',))
    def echo(self):
        content_type = request.mimetype
        msg = ""
        if content_type == 'application/json':
            data_dict = self.handle_json(request.data)
            if data_dict is None: return abort(400)
            msg = 'JSON\n{}'.format(data_dict)
            return Response(msg, status=200, mimetype='text/plain')
        elif content_type == 'text/plain':
            txt_data = request.data
            msg = 'Plain Text\n{}'.format(txt_data)
        elif content_type == 'text/csv':
            try:
                csv_unicode_io = StringIO(request.data.decode('unicode-escape'))
                data_df = pd.read_csv(csv_unicode_io)
                msg = 'CSV\n{}'.format(data_df.to_string())
            except Exception as e:
                print e.message
                return abort(400)
        else:
            return abort(400)

        return Response(msg, status=200, mimetype=content_type)
