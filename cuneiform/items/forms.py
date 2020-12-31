#forms.py items
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired


class UpdateForm(FlaskForm):
    id = IntegerField('Id of Item to Buy:', validators=[DataRequired()])
#shold i call this buy grocery? TO DO
class UpdateNameForm(UpdateForm):

    name = StringField('Name of Item:')
    submit = SubmitField('Update')

class UpdateStatusForm(UpdateForm):

    #name = StringField('Name of Item:')
    is_bought = SubmitField('Mark as Bought')


class AddForm(FlaskForm):

    name = StringField('Name of Item:')
    #is_bought = BooleanField('Purchased')
    #user_id = IntegerField('Created by User: ')
    submit = SubmitField('Add Item')
    #timestamp TO DO
    #household id? TO DO
