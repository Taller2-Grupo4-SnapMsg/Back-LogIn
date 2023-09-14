# user_repository.py

"""
This module is for the repository layer of the REST API for the login backend.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repository.tables.users import Base
from repository.errors import DuplicatedPrimaryKey
from repository.queries.queries import get_user_by_mail as get_user_by_mail_db
from repository.queries.queries import get_user_by_username as get_user_by_username_db
from repository.queries.queries import create_user as create_user_db
from repository.queries.queries import get_all_users as get_all_users_db
from repository.queries.queries import delete_user as delete_user_db

# We connect to the database using the ORM defined in tables.py
engine = create_engine(
    "postgresql://cwfvbvxl:jtsNDRjbVqGeBgYcYvxGps3LLlX_t-P5@berry.db.elephantsql.com:5432/cwfvbvxl"
)

# Create the tables in the database
Base.metadata.create_all(engine)

# Session is the handle of the database
Session = sessionmaker(bind=engine)
session = Session()
TIMEOUT = 60
GET_USERS_URL = "https://bdd-users-api.onrender.com/users"
GET_USER_BY_NICK_URL = "https://bdd-users-api.onrender.com/get_user_by_username"
GET_USER_BY_MAIL_URL = "https://bdd-users-api.onrender.com/get_user_by_mail"
DELETE_USER_BY_MAIL_URL = "https://bdd-users-api.onrender.com/delete_user_by_mail"
REGISTER_USER_URL = "https://bdd-users-api.onrender.com/register_new_user"

# TODO: Put an env variable for local and production database.
# TODO: delete mock_db
mock_db = {}


def register_user(
    email: str,
    password: str,
    nickname: str,
    data: dict,
):
    """
    This function that adds a user to the database.

    :param user: The user to register.
    :return: confirmation JSON message.
    """

    user = create_user_db(session, email, password, nickname, data)
    if user is None:
        raise DuplicatedPrimaryKey()
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


def get_user_nickname(nickname: str):
    """
    This function retrieves an user by nickname.

    :param nickname: The nickname of the user to retrieve.
    :return: The user's information.
    """
    user = get_user_by_username_db(session, nickname)
    if user is None:
        raise KeyError()
    return user


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
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    delete_user_db(session, user.id)


def get_user_collection():
    """
    This is a debug function that gets all the users from the db
    :return: A list of all the users in the db
    """
    return get_all_users_db(session)


session.close()
