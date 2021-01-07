# cuneiform/users/items.py

from flask import render_template, redirect, url_for, request, flash
from cuneiform import db
from cuneiform.models import Item, User
from cuneiform.items.forms import AddForm, UpdateForm, UploadForm
from flask_login import current_user, login_required
from . import items_blueprint
from flask_uploads import configure_uploads, IMAGES, UploadSet
from cuneiform.services.ocrservice import OcrService
import requests
from flask_injector import FlaskInjector
from injector import inject
from cuneiform.dependencies import configure

# from ocrservice import worker

# work around for providing user feedback, as CSS modal fade class
# doesn't display the raised validation errors
def flash_errors(form):
    """Flashes form errors"""
    for errors in form.errors.items():
        for error in errors:
            flash(f"Error: {error}")


# GET /items/create
@items_blueprint.route("/create", methods=["GET"])
@login_required
def create():
    form = AddForm()
    return render_template("add_item.html.j2", form=form)


# POST /items
@items_blueprint.route("", methods=["POST"])
@login_required
def store():

    add_form = AddForm()
    if add_form.validate_on_submit():
        name = request.form["name"]
        user_id = current_user.id
        # Add new item to database
        new_item = Item(name, user_id)
        db.session.add(new_item)
        db.session.commit()

    flash_errors(add_form)

    return redirect(url_for("items.index"))


# POST /items/shoppinglist
@inject
@items_blueprint.route("/shoppinglist", methods=["POST"])
@login_required
def store_many(service: OcrService):

    upload_form = UploadForm()
    if upload_form.validate_on_submit():
        image_file = upload_form.image.data
        image = image_file.read()
        items_list, err_code = service.process_image(image)

        if items_list == None:
            # Could not process the image, flash specific err_code
            flash(service.err_code_to_message.get(err_code))
            return redirect(url_for("items.index"))

        user_id = current_user.id

        for item in items_list:
            name = item
            new_item = Item(name, user_id)
            db.session.add(new_item)
            db.session.commit()

        return redirect(url_for("items.index"))

    flash_errors(upload_form)

    return redirect(url_for("items.index"))  # image not provided


# GET items
@items_blueprint.route("", methods=["GET"])
@login_required
def index():

    add_form = AddForm()
    update_form = UpdateForm()
    upload_form = UploadForm()
    # Grab a list of items from database.
    items = (
        db.session.query(User, Item)
        .filter(
            User.id == Item.user_id,
            Item.user_id == current_user.id,
            Item.is_bought == False,
        )
        .all()
    )
    return render_template(
        "items/items_list.html.j2",
        items=items,
        add_form=add_form,
        update_form=update_form,
        upload_form=upload_form,
    )


# GET ITEMS/shoppinglist
@items_blueprint.route("/shoppinglist", methods=["GET"])
@login_required
def purchases():
    # Grab a list of items from database.
    items = (
        db.session.query(User, Item)
        .filter(
            User.id == Item.user_id,
            Item.user_id == current_user.id,
            Item.is_bought == True,
        )
        .all()
    )
    return render_template("items/purchases_list.html.j2", items=items)


# GET /items/<id>/edit form
@items_blueprint.route("/<id>/edit", methods=["GET"])
@login_required
def edit(id):
    item = Item.query.get(id)
    form = UpdateForm()
    return render_template("buy_items.html.j2", form=form, item=item)


# /items/<id>
@items_blueprint.route("/<id>/update", methods=["POST"])
@login_required
def update(id):

    update_form = UpdateForm()
    item = Item.query.get(id)

    if update_form.validate_on_submit():
        item.name = request.form["name"]
        item.is_bought = bool(request.form["is_bought"])
        flash("Item Status Updated Successfully")
        db.session.commit()

    flash_errors(update_form)

    return redirect(url_for("items.index"))
