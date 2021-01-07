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
            # flash(f"in field {getattr(form, field).label.text}")


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
    # TO DO -> parse incoming request into some kind of object
    # Then validate the request (rules for validation) -> regex or alternative
    #
    add_form = AddForm()
    if add_form.validate_on_submit():
        name = request.form["name"]
        # is_bought = request.form['is_bought']
        user_id = current_user.id
        # Add new item to database
        new_item = Item(name, user_id)
        db.session.add(new_item)
        db.session.commit()

    flash_errors(add_form)

    return redirect(url_for("items.index"))


# POST /items
@inject
@items_blueprint.route("/storemany", methods=["POST"])
@login_required
def store_many(service: OcrService):
    # TO DO -> parse incoming request into some kind of object
    # Then validate the request (rules for validation) -> regex or alternative
    #
    upload_form = UploadForm()
    print("validating form")
    if upload_form.validate_on_submit():
        image_file = upload_form.image.data
        # if image_file is None:
        #    flash("Please upload an image only")
        #    return redirect(url_for("items.index"))
        image = image_file.read()
        # s = requests.Session()
        # service(s)
        items_list, err_code = service.process_image(image)

        if items_list == None:
            flash(service.err_code_to_message.get(err_code))
            return redirect(url_for("items.index"))

        print(f"items list {items_list}")
        print(f"err_code {err_code}")
        user_id = current_user.id
        print(f"user id is {user_id}")
        # Add new item to database
        for item in items_list:
            name = item
            new_item = Item(name, user_id)
            db.session.add(new_item)
            db.session.commit()

        return redirect(url_for("items.index"))

    flash_errors(upload_form)

    return (redirect(url_for("items.index")), 422)  # image not provided


@items_blueprint.route("")
@login_required
def index():
    # Grab a list of items from database.
    add_form = AddForm()
    # update_name_form = UpdateNameForm()
    # update_status_form = UpdateStatusForm()
    update_form = UpdateForm()
    upload_form = UploadForm()
    # items = Item.query.filter_by(user_id=current_user.id)
    items = (
        db.session.query(User, Item)
        .filter(User.id == Item.user_id, Item.user_id == current_user.id)
        .all()
    )
    return render_template(
        "items/items_list.html.j2",
        items=items,
        add_form=add_form,
        update_form=update_form,
        upload_form=upload_form,
    )


# /items/edit
@items_blueprint.route("<id>/edit", methods=["GET"])
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
    # update_name_form = UpdateNameForm()
    # update_status_form = UpdateStatusForm()
    #
    item = Item.query.get(id)
    #
    # is_update_status, is_update_name = False, False
    # # check if the form label names are found in the request form
    # check_fields = [request.form.get(field.name) for field in /
    # update_status_form]
    # is_update_status = not None in check_fields
    #
    # check_fields = [request.form.get(field.name) for field in /
    #  update_name_form]
    # is_update_name = not None in check_fields

    # if is_update_status and
    if update_form.validate_on_submit():
        # if 'is_bought' in request.form and /
        # update_status_form.validate_on_submit():
        # print("setting bought")
        # print(request.form)
        item.name = request.form["name"]
        item.is_bought = bool(request.form["is_bought"])
        flash("Item Status Updated Successfully")
        db.session.commit()

    # id = update_form.id.data

    # if is_update_name and
    # if update_name_form.validate_on_submit():
    #     print("updating name")
    #     item.name = request.form['name']
    #     flash("Item Name Updated Successfully")

    flash_errors(update_form)

    # item = Item.query.get(request.form.get('id'))

    # item.is_bought = True

    return redirect(url_for("items.index"))
