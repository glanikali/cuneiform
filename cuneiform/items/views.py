# cuneiform/users/items.py

from flask import Blueprint, render_template, redirect, url_for
from cuneiform import db
from cuneiform.models import Item
from cuneiform.items.forms import AddForm, UpdateForm

items_blueprint = Blueprint('items', __name__,
                            template_folder='templates/items')


@items_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()

    if form.validate_on_submit():
        name = form.name.data
        is_bought = form.is_bought.data
        user_id = form.user_id.data
        # Add new item to database
        new_item = Item(name,user_id)
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for('items.list'))

    return render_template('add_item.html.j2',form=form)

@items_blueprint.route('/list')
def list():
    # Grab a list of puppies from database.
    items = Item.query.all()
    return render_template('list_items.html.j2', items=items)

@items_blueprint.route('/update', methods=['GET', 'POST'])
def update():

    form = UpdateForm()

    if form.validate_on_submit():
        id = form.id.data
        item = Item.query.get(id)
        item.is_bought = True
        db.session.commit()

        return redirect(url_for('items.list'))
    return render_template('buy_items.html.j2',form=form)
