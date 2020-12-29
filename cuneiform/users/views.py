# cuneiform/users/view.py

from flask import (Blueprint, render_template, redirect,
                    url_for,request,flash,abort)
from flask_login import login_user, login_required, logout_user
from cuneiform import db,app
from cuneiform.models import User
from cuneiform.users.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint('users', __name__,
                            template_folder='templates/users')


@users_blueprint.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html.j2')

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('index'))

# TO DO, if user logs in but user doesn't exist no message is passed
@users_blueprint.route('login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check password and username provided
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in Successfully!')
            # Handle if user was trying to access a restricted page
            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('index')

            return redirect(next)

    return render_template('login.html.j2', form=form)

# if email is incorrect format no message provided
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Thanks for registration!")
            return redirect(url_for('users.login'))

        # if username or email are not unique    
        except IntegrityError:
            db.session.rollback()
            flash("User or Email already exists")

    return render_template('register.html.j2', form=form)
#
# @users_blueprint.route('/add', methods=['GET', 'POST'])
# def add():
#
#     form = AddForm()
#
#     if form.validate_on_submit():
#         name = form.name.data
#         #household_id = form.household_id_id.data
#         #email/password
#         # Add new user to database
#         new_user = User(name) #,household_id)
#         db.session.add(new_user)
#         db.session.commit()
#
#         return redirect(url_for('users.list'))
#
#     return render_template('add_user.html.j2',form=form)
#
#
# @users_blueprint.route('/list')
# def list():
#     # Grab a list of puppies from database.
#     users = User.query.all()
#     return render_template('list_users.html.j2', users=users)
