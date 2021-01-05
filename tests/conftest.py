import pytest
from cuneiform import create_app, db
from cuneiform.models import User


@pytest.fixture(scope='module')
def new_user():
    user = User(email='ishan@gmail.com',username='ishan', password='FlaskIsAwesome')
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(email='ishan@gmail.com',username='ishan', password='FlaskIsAwesome')
    user2 = User(email='ishansfriend@gmail.com', username='friend', password='P@55w0rd')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()
