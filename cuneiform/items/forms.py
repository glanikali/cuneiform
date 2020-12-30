#forms.py items

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField



#shold i call this buy grocery? TO DO
class UpdateForm(FlaskForm):

    #id = IntegerField('Id of Item to Buy:')
    name = StringField('Name of Item:')
    submit = SubmitField('Buy Item')

class AddForm(FlaskForm):

    name = StringField('Name of Item:')
    #is_bought = BooleanField('Purchased')
    #user_id = IntegerField('Created by User: ')
    submit = SubmitField('Add Item')
    #timestamp TO DO
    #household id? TO DO
