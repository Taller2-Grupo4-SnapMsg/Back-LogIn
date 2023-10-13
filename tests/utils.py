# utils.py
"""
This is a module that contains all the functions that are used on the tests.
"""
from service.user import User
from service.user import remove_user_email
from service.errors import UserNotFound

EMAIL = "real_email@gmail.com"
USERNAME = "real_username"
PASSWORD = "Real_password123"


def save_test_user_to_db(email=EMAIL, username=USERNAME, password=PASSWORD):
    """
    This function saves the test user to the database.
    """
    user = create_generic_user(email, username, password)

    user.save()


def create_generic_user(email=EMAIL, username=USERNAME, password=PASSWORD):
    """
    Function to create a generic user that is used on the tests
    """
    return User(
        email=email,
        password=password,
        name="Real_name",
        surname="Real_surname",
        username=username,
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
        location="Real_location",
        blocked=False,
    )


def create_multiple_generic_users(ammount=10):
    """
    Function to create multiple generic users that are used on the tests
    """
    for i in range(0, ammount):
        save_test_user_to_db(email=EMAIL + str(i), username=USERNAME + str(i))


def remove_multiple_generic_users(ammount=10):
    """
    Function to remove multiple generic users that are used on the tests
    """
    for i in range(0, ammount):
        remove_user_email(EMAIL + str(i))


def remove_test_user_from_db(email=EMAIL):
    """
    This function removes the test user from the database.
    """
    try:
        remove_user_email(email)
    except UserNotFound:
        return
