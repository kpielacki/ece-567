from flask import (Flask, redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_admin import (Admin, BaseView, expose)
import flask_login
import os
import sys


class DummyHome(BaseView):

    @expose('/')
    def index(self):
        return redirect('/home')


# Import environment variables
try:
    SECRET_KEY = os.environ['SECRET_KEY']
    SQL_SERVER = os.environ['SQL_SERVER']
    SQL_USER = os.environ['SQL_USER']
    SQL_PASSWD = os.environ['SQL_PASSWD']
    SQL_HOST = os.environ['SQL_HOST']
    SQL_DB = os.environ['SQL_DB']
except Exception as e:
    print 'Environment variable {} not set, review README.md'.format(e.message)
    sys.exit(-1)


name = 'Health Monitoring'
server = Flask(name, static_folder='assets')
server.config['SECRET_KEY'] = SECRET_KEY
server.config['SQLALCHEMY_DATABASE_URI'] = '{}://{}:{}@{}/{}'.format(
    SQL_SERVER, SQL_USER, SQL_PASSWD, SQL_HOST, SQL_DB)
server.config['SQLALCHEMY_ECHO'] = False
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
admin = Admin(
    name=name,
    static_url_path='/assets',
    index_view=DummyHome(name='', url='/'),
    base_template='base.html',
    template_mode='bootstrap3'
)
db = SQLAlchemy(server)
admin.init_app(server)

login_manager = flask_login.LoginManager()
login_manager.init_app(server)

with server.app_context():
    db.Model.metadata.bind = db.engine
    import hooks
