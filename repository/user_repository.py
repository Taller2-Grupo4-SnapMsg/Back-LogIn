# user_repository.py

"""
This module is for the repository layer of the REST API for the login backend.
"""

mock_db = {}  # Mock database, in reality this would be a real database.


def register(email: str, password: str):
    """
    This function is a test function that mocks user registration.

    :param user: The user to register.
    :return: Status code with a JSON message.
    """
    if email in mock_db:
        raise KeyError()
    mock_db[email] = {"email": email, "password": password}
    return {"message": "Registration successful"}


def get_user(email: str):
    """
    This function is a test function that mocks retrieving a user.

    :param email: The email of the user to retrieve.
    :return: The user's information.
    """
    if email not in mock_db:
        raise KeyError()
    return mock_db[email]


def update_user(email: str, new_password: str):
    """
    This function is a test function that mocks updating a user.

    :param email: The email of the user to update.
    :param user: The user's new information.
    :return: Status code with a JSON message.
    """
    if email not in mock_db:
        raise KeyError()
    mock_db[email]["password"] = new_password
    return {"message": "Update successful"}
