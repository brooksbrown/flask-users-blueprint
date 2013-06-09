import random, string

from flask import Blueprint, request, render_template, redirect, abort

from models import User, FLUserWrapper
from forms import LoginForm, RegistrationForm, EmailAuthInitiateForm


from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug import generate_password_hash, check_password_hash

from database import db
app = Blueprint('users', __name__, template_folder='templates', url_prefix='/users')

@app.route('/<int:user_id>')
def user_view(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template("user.html", user = user)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User()
        #Generate a username
        new_username = form.email.data.split('@')[0]
        i = 0
        users_with_name = 1
        while users_with_name is not None:
            users_with_name = User.query.filter_by(username=new_username).first()
            if users_with_name is not None:
                i = i + 1
                new_username = new_username + "-" + str(i)

        new_user.username    = new_username
        new_user.email = form.email.data
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('registration.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if not current_user.is_anonymous():
        return redirect('/')
    form = LoginForm()

    if form.validate_on_submit():
        # login and validate the user...
        user = FLUserWrapper(form.user)
        login_user(user)
        return redirect('/')
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route("/email-auth", methods=['GET', 'POST'])
def email_auth():

    form = EmailAuthInitiateForm()

    if form.validate_on_submit():
        reset_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(120))
        print 'reset_key:' + reset_key
        form.user.email_auth_hash = generate_password_hash(reset_key)
        db.session.commit()
        return redirect('/')
    return render_template('email-auth.html', form=form)


@app.route("/email-auth-confirm", methods=['GET', 'POST'])
def password_reset_change():
    if 'id' in request.args and 'reset-key' in request.args:
        user_id = request.args.get('id')
        reset_key = request.args.get('reset-key')
        user = User.query.filter_by(id=user_id).first()
        print user
        if check_password_hash(user.email_auth_hash, reset_key):
            user.reset_password_hash = ''
            db.session.commit()
            user = FLUserWrapper(user)
            login_user(user)
            return redirect('/')
    abort(403)


def user_debug():
    out = "";
    if current_user.is_anonymous():
        out += "Not Logged In"
    else:
        out += "Logged In "
        out += "(user id : " + str(current_user._user.id) + ") "
        out += "(username : " + current_user._user.username + ") "
        out += "(email : " + current_user._user.email + ") "
        out += "(roles : "
        for role in current_user._user.roles:
            out += role.name + ", "
        out += ") "
    return out