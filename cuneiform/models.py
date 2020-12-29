# MODELS.PY
from cuneiform import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    #email TO DO
    #username TO DO
    # QUESTION: should households be one households to many users? -> It is not One user to One household right?
    #TO DOhousehold_id = db.Column(db.Integer,db.ForeignKey('households.id'))
    groceries = db.relationship('Item',backref='user',lazy='dynamic') #one to many -> will be list

    def __init__(self,name):
        self.name = name
        #self.household_id = household_id

    def __repr__(self):
        return f"User Name: {self.name}    User Id: {self.id}"


class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    is_bought = db.Column(db.Boolean)
    #is_bought = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #timestamp TO DO
    #HouseholdF.K -> redundant, normalize?

    def __init__(self,name,user_id):
        self.name = name
        self.user_id = user_id
        self.is_bought = False

    def __repr__(self):
        return f"Item Name: {self.name}    Wanted By: {self.user_id}   Item Id: {self.id}   Item Bought: {self.is_bought}"
