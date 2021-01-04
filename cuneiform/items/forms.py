#forms.py items
from cuneiform.models import Item

from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, ValidationError
from wtforms.widgets import HiddenInput
from wtforms.validators import InputRequired, DataRequired, Length
from flask_login import current_user

class AddForm(FlaskForm):

    min, max = Item.name_min_len, Item.name_max_len
    name = StringField('Name of Item:', validators=[InputRequired(message="Name required"),
                                        Length(min=min, max=max,
                                        message=f"Name must be between {min} and {max} characters")])
    #is_bought = BooleanField('Purchased')
    #user_id = IntegerField('Created by User: ')
    submit = SubmitField('Add Item')




    #timestamp TO DO
    #household id? TO DO


class UpdateForm(FlaskForm):

    # following field is hidden in the template
    id = IntegerField('Id of Item to Buy:', validators=[DataRequired()])
    min, max = Item.name_min_len, Item.name_max_len
    name = StringField('Name of Item:', validators=[InputRequired(message="Name required"),
                                        Length(min=min, max=max,
                                        message=f"Name must be between {min} and {max} characters")])
    is_bought = BooleanField('Is Bought', default="checked")
    submit = SubmitField('Update')

    def validate_id(self,field):
        id = field.data
        user = current_user
        item = Item.query.filter_by(id=id).first()


        if not item or item.user_id != user.id:
            print("cannot edit this item")
            raise ValidationError("Cannot edit this item")

        print(f"user id {user.id}, item id {item.id}")



# #shold i call this buy grocery? TO DO
# class UpdateNameForm(UpdateForm, AddForm):
#     is_bought = BooleanField('Is Bought')
#     submit = SubmitField('Update')
#
#
# class UpdateStatusForm(UpdateForm, AddForm):
#
#     #name = StringField('Name of Item:')
#     is_bought = BooleanField('Is Bought', default="checked")
#     submit = SubmitField('Mark as Bought')
