# user_repository.py

"""
This module is for the repository layer of the REST API for the login backend.
"""

import requests
from fastapi import HTTPException
from repository.errors import DatabaseTimeout

mock_db = {}  # Mock database, in reality this would be a real database.
TIMEOUT = 60
GET_USERS_URL = "https://bdd-users-api.onrender.com/users"
GET_USER_BY_NICK_URL = "https://bdd-users-api.onrender.com/get_user_by_username"
GET_USER_BY_MAIL_URL = "https://bdd-users-api.onrender.com/get_user_by_mail"
DELETE_USER_BY_MAIL_URL = "https://bdd-users-api.onrender.com/delete_user_by_mail"
REGISTER_USER_URL = "https://bdd-users-api.onrender.com/register_new_user"


def register_user(
    email: str,
    password: str,
    nickname: str,
    data: dict,
):
    """
    This function that adds a user to the database.

    :param user: The user to register.
    :return: Status code with a JSON message.
    """

    headers_request = {"accept": "application/json", "Content-Type": "application/json"}

    payload = {
        "username": nickname,
        "surname": data["surname"],
        "name": data["name"],
        "password": password,
        "email": email,
        "date_of_birth": data["date_of_birth"],
    }

    try:
        response = requests.post(
            REGISTER_USER_URL, json=payload, headers=headers_request, timeout=TIMEOUT
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response.json()["detail"]
            )
    except requests.exceptions.Timeout as error:
        raise DatabaseTimeout from error

    return {"message": "Registration successful"}


def get_user_email(email: str):
    """
    This function retrieves a user.

    :param email: The email of the user to retrieve.
    :return: The user's information.
    """

    try:
        response = requests.get(
            GET_USER_BY_MAIL_URL, params={"mail": email}, timeout=TIMEOUT
        )
        if (
            response.status_code != 200
        ):  # TO do: add more error handling so the exceptions are clear.
            raise KeyError()
    except requests.exceptions.Timeout as error:
        raise DatabaseTimeout from error
    return response.json()


def get_user_nickname(nickname: str):
    """
    This function retrieves an user by nickname.

    :param nickname: The nickname of the user to retrieve.
    :return: The user's information.
    """
    try:
        response = requests.get(
            GET_USER_BY_NICK_URL, params={"username": nickname}, timeout=TIMEOUT
        )
        if response.status_code != 200:
            raise KeyError()
    except requests.exceptions.Timeout as error:
        raise DatabaseTimeout from error
    return response.json()


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
    try:
        response = requests.delete(
            DELETE_USER_BY_MAIL_URL, params={"mail": email}, timeout=TIMEOUT
        )
        if response.status_code != 200:
            raise KeyError()
    except requests.exceptions.Timeout as error:
        raise DatabaseTimeout from error
    return {"message": "Delete successful"}


def get_user_collection():
    """
    This is a test for calling the data base API
    """
    timeout = 10
    try:
        response = requests.get(GET_USERS_URL, timeout=timeout)
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")
    return response.json()
