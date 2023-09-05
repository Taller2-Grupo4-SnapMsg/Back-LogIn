# user_tests.py

"""
This is the test module.
"""

from service.user import User


def test_user_login():
    """
    This function tests the user login.
    """
    user = User(email="real_email@gmail.com", password="Real_password123")

    user.save()

    assert user.login() == {"message": "Login successful"}
