from admin_app_config import db


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(320), nullable=False)
    user_group = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return 'Username: %s' % self.username
