"""
This file (test_core.py) contains the functional tests for the `core` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the `core` blueprint.
"""
from cuneiform import create_app


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        assert b"Welcome to Cuneiform, script your needs." in response.data
        assert b"Please login or register" in response.data


def test_home_page_post():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    flask_app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.post("/")
        assert response.status_code == 405
        assert b"Welcome to Cuneiform, script your needs." not in response.data


def test_home_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Cuneiform, script your needs." in response.data
    assert b"Please login or register" in response.data


def test_home_page_post_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post("/")
    assert response.status_code == 405
    assert b"Welcome to Cuneiform, script your needs." not in response.data
