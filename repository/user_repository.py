# user_repository.py

"""
This module is for the repository layer of the REST API for the login backend.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repository.tables.users import Base
from repository.queries.queries import get_user_by_mail as get_user_by_mail_db
from repository.queries.queries import get_user_by_username as get_user_by_username_db
from repository.queries.queries import create_user as create_user_db
from repository.queries.queries import get_all_users as get_all_users_db
from repository.queries.queries import delete_user as delete_user_db
from repository.queries.queries import update_user_password as update_user_password_db
from repository.queries.queries import update_user_admin as update_user_admin_db

# We connect to the database using the ORM defined in tables.py
engine = create_engine(os.environ.get("DB_URI"))

# Create the tables in the database
Base.metadata.create_all(engine)

# Session is the handle of the database
Session = sessionmaker(bind=engine)
session = Session()
TIMEOUT = 60


def register_user(
    email: str,
    password: str,
    username: str,
    data: dict,
):
    """
    This function that adds a user to the database.

    :param user: The user to register.
    :return: confirmation JSON message.
    """

    create_user_db(session, email, password, username, data)

    return {"message": "Registration successful"}


def get_user_email(email: str):
    """
    This function retrieves a user.

    :param email: The email of the user to retrieve.
    :return: The user's information.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    return user


def get_user_username(username: str):
    """
    This function retrieves an user by username.

    :param username: The username of the user to retrieve.
    :return: The user's information.
    """
    user = get_user_by_username_db(session, username)
    if user is None:
        raise KeyError()
    return user


def update_user_password(email: str, new_password: str):
    """
    This function is a test function that mocks updating a user.

    :param email: The email of the user to update.
    :param user: The user's new information.
    :return: Status code with a JSON message.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    update_user_password_db(session, user.id, new_password)


def remove_user(email: str):
    """
    This is used for deleting a user from the data base.

    :param email: The email used to identify the user.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    delete_user_db(session, user.id)


def make_admin(email: str):
    """
    This is used for making a user admin.

    :param email: The email used to identify the user.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    update_user_admin_db(session, user.id, True)


def remove_admin_status(email: str):
    """
    This is used for removing a user's admin status.

    :param email: The email used to identify the user.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    update_user_admin_db(session, user.id, False)


def get_user_collection():
    """
    This is a debug function that gets all the users from the db
    :return: A list of all the users in the db
    """
    return get_all_users_db(session)


session.close()
