# cuneiform/users/view.py

from flask import Blueprint, render_template, redirect, url_for
from cuneiform import db
from cuneiform.models import User
from cuneiform.users.forms import AddForm

users_blueprint = Blueprint('users', __name__,
                            template_folder='templates/users')


@users_blueprint.route('/add', methods=['GET', 'POST'])
def add():

    form = AddForm()

    if form.validate_on_submit():
        name = form.name.data
        #household_id = form.household_id_id.data
        #email/password
        # Add new user to database
        new_user = User(name) #,household_id)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('users.list'))

    return render_template('add_user.html.j2',form=form)


@users_blueprint.route('/list')
def list():
    # Grab a list of puppies from database.
    users = User.query.all()
    return render_template('list_users.html.j2', users=users)
