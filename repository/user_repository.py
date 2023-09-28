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
from repository.queries.queries import update_user_bio as update_user_bio_db
from repository.queries.queries import update_user_name as update_user_name_db
from repository.queries.queries import (
    update_user_date_of_birth as update_user_date_of_birth_db,
)
from repository.queries.queries import update_user_last_name as update_user_last_name_db
from repository.queries.queries import update_user_avatar as update_user_avatar_db
from repository.queries.queries import update_user_admin as update_user_admin_db
from repository.queries.queries import create_follow as create_follow_db
from repository.queries.queries import get_followers as get_followers_db
from repository.queries.queries import get_following as get_following_db
from repository.queries.queries import (
    get_following_relations as get_following_relations_db,
)
from repository.queries.queries import get_following_count as get_following_count_db
from repository.queries.queries import get_followers_count as get_followers_count_db
from repository.queries.queries import remove_follow as remove_follow_db
from repository.queries.queries import is_following as is_following_db

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


def create_follow(email: str, email_to_follow: str):
    """
    This is used for creating a follow relation between two users.

    :param email: The email of the user that wants to follow.
    :param email_to_follow: The email of the user that is being followed.
    """
    follow = create_follow_db(session, email, email_to_follow)
    if follow is None:
        raise KeyError()


def get_followers(user_id: int):
    """
    This is used for getting the followers of a user.

    :param username: The user's id.
    """
    return get_followers_db(session, user_id)


def get_following(user_id: int):
    """
    This is used for getting the following of a user.

    :param user_id: The user's id.
    """
    return get_following_db(session, user_id)


def is_following(user_id: int, user_id_to_check_if_following: int):
    """
    This is used for getting the following of a user.

    :param user_id: The user's id.
    """
    return is_following_db(session, user_id, user_id_to_check_if_following)


def get_following_relations():
    """
    This is used for getting the following relations between users.
    """
    return get_following_relations_db(session)


def get_following_count(user_id: int):
    """
    This is used for getting the number of users a user is following.

    :param user_id: The user's id.
    """
    return get_following_count_db(session, user_id)


def get_followers_count(user_id: int):
    """
    This is used for getting the number of followers a user has.

    :param username: The username of the user.
    """
    return get_followers_count_db(session, user_id)


def remove_follow(user_id: int, user_id_to_unfollow: int):
    """
    This is used for removing a follow relation between two users.

    :param username: The username of the user that wants to unfollow.
    :param username_to_unfollow: The username of the user that is being unfollowed.
    """
    remove_follow_db(session, user_id, user_id_to_unfollow)


def get_user_collection():
    """
    This is a debug function that gets all the users from the db
    :return: A list of all the users in the db
    """
    return get_all_users_db(session)


def update_user_bio(email: str, bio: str):
    """
    This is used for updating a user's bio.

    :param email: The email used to identify the user.
    :param bio: The bio to update.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    update_user_bio_db(session, user.id, bio)


def update_user_last_name(email: str, last_name: str):
    """
    This is used for updating a user's last_name.

    :param email: The email used to identify the user.
    :param last_name: The last_name to update.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    update_user_last_name_db(session, user.id, last_name)


def update_user_name(email: str, name: str):
    """
    This is used for updating a user's name.

    :param email: The email used to identify the user.
    :param name: The name to update.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    update_user_name_db(session, user.id, name)


def update_user_date_of_birth(email: str, date_of_birth: str):
    """
    This is used for updating a user's date_of_birth.

    :param email: The email used to identify the user.
    :param date_of_birth: The date_of_birth to update.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    update_user_date_of_birth_db(session, user.id, date_of_birth)


def update_user_avatar(email: str, avatar: str):
    """
    This is used for updating a user's avatar.

    :param email: The email used to identify the user.
    :param avatar: The avatar to update.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    update_user_avatar_db(session, user.id, avatar)


session.close()
