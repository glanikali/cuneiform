# cuneiform/users/view.py

from flask import (Blueprint, render_template, redirect,
                    url_for,request,flash,abort, session)
from flask_login import login_user, login_required, logout_user, current_user
from cuneiform import db#,app
from cuneiform.models import User
from cuneiform.users.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from . import users_blueprint


@users_blueprint.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html.j2')

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('recipes.index'))

# TO DO, if user logs in but user doesn't exist no message is passed
@users_blueprint.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Grab the user
        user = User.query.filter_by(email=form.email.data).first()
        #Log in the user
        login_user(user)
        flash('Logged in Successfully!')
        print(f"User id is {current_user.id}")
        # Handle if user was trying to access a restricted page
        next = request.args.get('next')

        if next == None or not next[0] == '/':
            next = url_for('recipes.index')

        return redirect(next)

    return render_template('users/login.html.j2', form=form)

# if email is incorrect format no message provided
@users_blueprint.route('/register', methods=['GET'])
def show_registration():
    form = RegistrationForm()

    return render_template('users/register.html.j2', form=form)

# if email is incorrect format no message provided
@users_blueprint.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registration!")
        return redirect(url_for('users.login'))

    # if form.is_submitted() and not form.validate():
    #     session['formdata'] = request.form
    #     return redirect(url_for('users.show_registration'))

    return (render_template('users/register.html.j2', form=form), 422)
