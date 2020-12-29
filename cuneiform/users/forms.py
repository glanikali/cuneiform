#forms.py users

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class AddForm(FlaskForm):

    name = StringField('Name of User:')
    #TO DO household = IntegerField('Household ID:')
    submit = SubmitField('Add User')
