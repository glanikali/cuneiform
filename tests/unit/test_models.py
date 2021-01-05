"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from cuneiform.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hash, authenticated, and role fields are defined correctly
    """
    user = User('ishan@gmail.com', 'ishan', 'FlaskIsAwesome')
    assert user.email == 'ishan@gmail.com'
    assert user.username == 'ishan'
    assert user.password_hash != 'FlaskIsAwesome'


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hash, authenticated, and role fields are defined correctly
    """
    assert new_user.email == 'ishan@gmail.com'
    assert new_user.password_hash != 'FlaskIsAwesome'
    assert new_user.username == 'ishan'


def test_setting_password(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_user.set_password('MyNewPassword')
    assert new_user.password_hash != 'MyNewPassword'
    assert new_user.check_password('MyNewPassword')
    assert not new_user.check_password('MyNewPassword2')
    assert not new_user.check_password('FlaskIsAwesome')


def test_user_id(new_user):
    """
    GIVEN an existing User
    WHEN the ID of the user is defined to a value
    THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
    """
    new_user.id = 17
    assert isinstance(new_user.get_id(), str)
    assert not isinstance(new_user.get_id(), int)
    assert new_user.get_id() == '17'
