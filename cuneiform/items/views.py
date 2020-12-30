# cuneiform/users/items.py

from flask import Blueprint, render_template, redirect, url_for, request
from cuneiform import db
from cuneiform.models import Item
from cuneiform.items.forms import AddForm, UpdateForm

items_blueprint = Blueprint('items', __name__,
                            template_folder='templates/items')


# @items_blueprint.route('/add', methods=['GET', 'POST'])
# def add():
#     form = AddForm()
#
#     if form.validate_on_submit():
#         name = form.name.data
#         #is_bought = form.is_bought.data
#         user_id = form.user_id.data
#         # Add new item to database
#         new_item = Item(name,user_id)
#         db.session.add(new_item)
#         db.session.commit()
#
#         return redirect(url_for('items.list'))
#
#     return render_template('add_item.html.j2',form=form)

#GET /items/create
@items_blueprint.route('/create', methods=['GET'])
def create():
    form = AddForm()
    return render_template('add_item.html.j2',form=form)

#POST /items
@items_blueprint.route('', methods=['POST'])
def store():
    # TO DO -> parse incoming request into some kind of object
    # Then validate the request (rules for validation) -> regex or alternative
    #
    name = request.form['name']
    #is_bought = request.form['is_bought']
    user_id = request.form['user_id']
    # Add new item to database
    new_item = Item(name,user_id)
    db.session.add(new_item)
    db.session.commit()

    return redirect(url_for('items.index'))



@items_blueprint.route('')
def index():
    # Grab a list of puppies from database.
    items = Item.query.all()
    return render_template('list_items.html.j2', items=items)



#/items/edit
@items_blueprint.route('<id>/edit', methods=['GET'])
def edit(id):
    item = Item.query.get(id)
    form = UpdateForm()
    return render_template('buy_items.html.j2',form=form, item=item)

#/items/<id>
@items_blueprint.route('/<id>/update', methods=['POST'])
def update(id):

    #id = form.id.data
    item = Item.query.get(id)
    item.is_bought = True
    db.session.commit()

    return redirect(url_for('items.index'))
