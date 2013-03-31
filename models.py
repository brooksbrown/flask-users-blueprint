from database import db

from werkzeug import generate_password_hash, check_password_hash

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

    def __repr__(self):
        return self.name

roles = db.Table('roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    username = db.Column(db.String(16))
    password = db.Column(db.String(60))
    roles = db.relationship('Role', secondary=roles, backref=db.backref('users', lazy='dynamic'))
    email_auth_hash = db.Column(db.String(120))

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def has_role(self, rolename):
        for role in self.roles:
            if role.name == rolename:
                return True
        return False


    def __repr__(self):
        return self.username

# Flask-Login User Object Wrapper
class FLUserWrapper(object):
    def __init__(self, user):
        self._user = user

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self._user.id)

