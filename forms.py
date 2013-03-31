from flask.ext.wtf import Form, TextField, PasswordField, validators, BooleanField, html5, HiddenField
from models import User

class LoginForm(Form):
    email = TextField('Email Address', [
        validators.Required()
    ])
    password = PasswordField('Password', [
        validators.Required()
    ])


    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):

        form_validation = Form.validate(self)
        if not form_validation:
            return False
        user = User.query.filter_by(
            email=self.email.data).first()
        if user is None:
            self.email.errors.append('Email not registered')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class RegistrationForm(Form):
    email = html5.EmailField('Email Address', [
        validators.Required(),
    ])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):

        form_validation = Form.validate(self)
        if not form_validation:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            self.email.errors.append('Email is already registered')
            return False


        return True

class EmailAuthInitiateForm(Form):
    email = html5.EmailField('Email Address', [
        validators.Required()
    ])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        form_validation = Form.validate(self)
        if not form_validation:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append('Email is not registered')
            return False

        self.user = user
        return True

