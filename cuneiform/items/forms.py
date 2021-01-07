# forms.py items
from cuneiform.models import Item
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import InputRequired, DataRequired, Length
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES


class AddForm(FlaskForm):

    min, max = Item.name_min_len, Item.name_max_len
    name = StringField(
        "Name of Item:",
        validators=[
            InputRequired(message="Name required"),
            Length(
                min=min,
                max=max,
                message=f"Name must be between {min} \
                                            and {max} characters",
            ),
        ],
    )

    submit = SubmitField("Add Item")


class UpdateForm(FlaskForm):

    # following field is hidden in the template
    id = IntegerField("Id of Item to Buy:", validators=[DataRequired()])
    min, max = Item.name_min_len, Item.name_max_len
    name = StringField(
        "Name of Item:",
        validators=[
            InputRequired(message="Name required"),
            Length(
                min=min,
                max=max,
                message=f"Name must be between {min} and {max} characters",
            ),
        ],
    )
    is_bought = BooleanField("Is Bought", default="checked")
    submit = SubmitField("Update")

    def validate_id(self, field):
        id = field.data
        user = current_user
        item = Item.query.filter_by(id=id).first()

        if not item or item.user_id != user.id:
            print("cannot edit this item")
            raise ValidationError("Cannot edit this item")

        print(f"user id {user.id}, item id {item.id}")


images = UploadSet("images", IMAGES)


class UploadForm(FlaskForm):
    image = FileField(
        "Image",
        validators=[
            FileRequired(),
            FileAllowed(
                ["jpg", "png", "jpeg"], "Images only (png, jpg and jpeg extensions)!"
            ),
        ],
    )
