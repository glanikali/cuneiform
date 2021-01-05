# MODELS.PY
from cuneiform import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    username_min_len, username_max_len = 3, 64
    email_min_len, email_max_len = 3, 254
    pass_min_len, pass_max_len = 6, 64
    pass_hash_len = 128


    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(email_max_len), unique=True, index=True)
    username = db.Column(db.String(username_max_len), unique=True, index=True)
    password_hash = db.Column(db.String(pass_hash_len))

    #email TO DO
    #username TO DO
    # QUESTION: should households be one households to many users? -> It is not One user to One household right?
    #TO DOhousehold_id = db.Column(db.Integer,db.ForeignKey('households.id'))
    groceries = db.relationship('Item',backref='user',lazy='dynamic') #one to many -> will be list

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        #self.household_id = household_id

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)
        
    def __repr__(self):
        return f"User Name: {self.username}    User Id: {self.id}"


class Item(db.Model):

    __tablename__ = 'items'

    name_min_len, name_max_len = 3, 64

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(name_max_len))
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
