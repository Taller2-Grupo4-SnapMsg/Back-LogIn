# user_repository.py

"""
This module is for the repository layer of the REST API for the login backend.
"""

mock_db = {}  # Mock database, in reality this would be a real database.


def register_user(
    email: str,
    password: str,
    nickname: str,
    data: dict,
):
    """
    This function is a test function that mocks user registration.

    :param user: The user to register.
    :return: Status code with a JSON message.
    """
    if email in mock_db:
        raise KeyError()
    mock_db[email] = {
        "email": email,
        "password": password,
        "name": data["name"],
        "surname": data["surname"],
        "nickname": nickname,
        "date_of_birth": data["date_of_birth"],
        "bio": data["bio"],
    }
    return {"message": "Registration successful"}


def get_user_email(email: str):
    """
    This function is a test function that mocks retrieving a user.

    :param email: The email of the user to retrieve.
    :return: The user's information.
    """
    if email not in mock_db:
        raise KeyError()
    return mock_db[email]


# This function won't work with our mocked dictionary, we need to change it later.
# when we have a real database with primary keys.
def get_user_nickname(nickname: str):
    """
    This function is a test function that mocks retrieving a user.

    :param nickname: The nickname of the user to retrieve.
    :return: The user's information.
    """
    if nickname not in mock_db:
        raise KeyError()
    return mock_db[nickname]


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


def remove_user(email: str):
    """
    This is used for deleting a user from the data base.

    :param email: The email used to identify the user.
    :return: Status code with a JSON message.
    """
    if email not in mock_db:
        raise KeyError()
    del mock_db[email]
    return {"message": "Delete successful"}
