from admin_app_config import db
import datetime
from flask import (abort, Response, request, redirect, flash, current_app)
from flask_admin import (BaseView, expose)
from flask_login import (current_user, login_user)
import json
import pandas as pd
from io import StringIO
from models import User
from werkzeug.security import (generate_password_hash, check_password_hash)
from wtforms.validators import (Length, Required, Regexp, Email)


def handle_json(data):
    """Attempts to create dictionary object from data request.
    Args:
        data (str): String representation of JSON.
    
    Returns:
        dict: If invalid JSON returns empty dictionary.
    """
    try:
        return json.loads(data)
    except Exception as e:
        return dict()


def validate_user(email, session_id):
    """Validates user and session.
    
    Args:
        email (str): User email for session.
        session_id (str): Logged in session ID.
    
    Returns:
        int: User ID or -1 if not valid user.
    """
    valid_user = User.query.filter_by(email=email).first()

    # Validate if user exists
    if not valid_user: return -1

    # Validate if user account is active
    if not(valid_user.active): return -1

    # TODO: Validate cookie or session ID tied to email
    return valid_user.id


class MobileLoginView(BaseView):

    def is_visible(self):
        return False

    @expose('/', methods=('POST',))
    def index(self):
        # To be converted to JSON and used to respond
        resp_dict = {'success': False, 'msg': None}

        # Get JSON data from mobile request
        data = handle_json(request.data)
        email = data.get('email', None)
        password = data.get('password', None)

        # Handle bad user request
        if email is None or password is None:
            resp_dict['success'] = False
            resp_dict['msg'] = 'Bad user request'
            return Response(resp_dict, status=400, mimetype='application/json')

        valid_user = User.query.filter_by(email=email).first()
        if not valid_user:
            # Attempt to create new user
            try:
                pw_hash = generate_password_hash(password)
                new_user = User(email=email, password=pw_hash,
                                user_group='user', active=True)
                db.session.add(new_user)
                db.session.commit()
                resp_dict['success'] = True
                resp_dict['msg'] = 'Created new account'
                return Response(json.dumps(resp_dict), status=200,
                                mimetype='application/json')
            except Exception as e:
                resp_dict['success'] = False
                resp_dict['msg'] = 'Something went wrong on our end'
                return Response(json.dumps(resp_dict), status=500,
                                mimetype='application/json')
        elif not(valid_user.active):
            # Account not activated
            resp_dict['success'] = False
            resp_dict['msg'] = 'Account not activated'
            return Response(json.dumps(resp_dict), status=403,
                            mimetype='application/json')
        elif not check_password_hash(valid_user.password, password):
            # Invalid email or password
            resp_dict['success'] = False
            resp_dict['msg'] = 'Invalid email or password'
            return Response(json.dumps(resp_dict), status=403,
                            mimetype='application/json')

        # Valid email and passord
        valid_user.login_date = datetime.datetime.now()
        db.session.commit()
        login_user(valid_user)
        resp_dict['success'] = True
        resp_dict['msg'] = 'Login successful'
        return Response(json.dumps(resp_dict), status=200,
                        mimetype='application/json')


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

    def handle_user_location_upload(self, df, user_id):
        return True

    def handle_user_steps_upload(self, df, user_id):
        return True

    @expose('/', methods=('GET',))
    def index(self):
        return Response('Mobile Handle', status=200, mimetype='text/html')

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
                csv_unicode_io = StringIO(
                    request.data.decode('unicode-escape'))
                data_df = pd.read_csv(csv_unicode_io)
                msg = 'CSV\n{}'.format(data_df.to_string())
            except Exception as e:
                print e.message
                return abort(400)
        else:
            return abort(400)

        return Response(msg, status=200, mimetype=content_type)

    @expose('/uploadtable/', methods=('POST',))
    def upload_table(self):
        resp_dict = {
            'success': False,
            'msg': None
        }

        # Only except JSON data
        if request.mimetype != 'application/json':
            resp_dict['success'] = False
            resp_dict['msg'] = 'Only JSON data accepted'
            json_resp = json.dumps(resp_dict)
            return Response(json_resp, status=400, mimetype='application/json')

        # Validate JSON
        data_dict = handle_json(request.data)
        if not data_dict:
            resp_dict['success'] = False
            resp_dict['msg'] = 'Invalid JSON data'
            json_resp = json.dumps(resp_dict)
            return Response(json_resp, status=400, mimetype='application/json')

        # Validate email and session
        email = data_dict.get('email', None)
        if email is None:
            resp_dict['success'] = False
            resp_dict['msg'] = 'No user found'
            json_resp = json.dumps(resp_dict)
            return Response(json_resp, status=403, mimetype='application/json')
        session_id = data_dict.get('session_id', None)
        if session is None:
            resp_dict['success'] = False
            resp_dict['msg'] = 'No session ID provided'
            json_resp = json.dumps(resp_dict)
            return Response(json_resp, status=403, mimetype='application/json')
        user_id = validate_user(email, session_id)

        if user_id < 0:
            resp_dict['success'] = False
            resp_dict['msg'] = 'Invalid email or session provided'
            json_resp = json.dumps(resp_dict)
            return Response(json_resp, status=403, mimetype='application/json')

        # Validate table entries
        table_data = data_dict.get('table_data', None)
        if table_data is None:
            resp_dict['success'] = False
            resp_dict['msg'] = 'No table data provided'
            json_resp = json.dumps(resp_dict)
            return Response(json_resp, status=400, mimetype='application/json')
        try:
            df = pd.DataFrame(table_data)
        except Exception:
            resp_dict['success'] = False
            resp_dict['msg'] = 'Improper table data format'
            json_resp = json.dumps(resp_dict)
            return Response(json_resp, status=400, mimetype='application/json')

        # Handle data upload per table differently
        table = data_dict.get('table', None)
        if table == 'user_location':
            self.handle_user_location_upload(df, user_id)
        elif table == 'user_steps':
            self.handle_user_steps_upload(df, user_id)

        # Response for tables that are not handled
        resp_dict['success'] = False
        resp_dict['msg'] = 'Unsupported table in POST request'
        json_resp = json.dumps(resp_dict)
        return Response(json_resp, status=400, mimetype='application/json')
