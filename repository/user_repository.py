# user_repository.py

"""
This module is for the repository layer of the REST API for the login backend.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repository.tables.users import Base
from repository.queries.user_queries import (
    create_user as create_user_db,
    delete_user as delete_user_db,
    get_all_users as get_all_users_db,
    get_user_by_mail as get_user_by_mail_db,
    get_user_by_username as get_user_by_username_db,
    update_user_password as update_user_password_db,
    update_user_admin as update_user_admin_db,
    update_user_bio as update_user_bio_db,
    update_user_last_name as update_user_last_name_db,
    update_user_name as update_user_name_db,
    update_user_date_of_birth as update_user_date_of_birth_db,
    update_user_avatar as update_user_avatar_db,
    update_user_location as update_user_location_db,
    update_user_blocked_status as update_user_blocked_status_db,
    delete_user_interests,
    add_user_interest,
    get_user_interests as get_user_interests_db,
    search_for_users as search_for_users_db,
    search_users_in_followers as search_users_in_followers_db,
    search_for_users_admins as search_for_users_admins_db,
    update_user_public_status as update_user_public_status_db,
)

from repository.queries.follow_queries import (
    create_follow as create_follow_db,
    get_followers as get_followers_db,
    get_following as get_following_db,
    get_following_relations as get_following_relations_db,
    get_following_count as get_following_count_db,
    get_followers_count as get_followers_count_db,
    remove_follow as remove_follow_db,
    is_following as is_following_db,
)

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
    This is used for checking if an user is following another user.

    :param user_id: The user's id.
    """
    return is_following_db(session, user_id, user_id_to_check_if_following)


def is_follower(user_id: int, user_id_to_check_if_follower: int):
    """
    This is used for checking if an user is a follower of another user.

    :param user_id: The user's id.
    """
    return is_following_db(session, user_id_to_check_if_follower, user_id)


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


def update_user_location(email: str, new_location: str):
    """
    This is used for updating a user's location.

    :param email: The email used to identify the user.
    :param new_location: The location to update.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    update_user_location_db(session, user.id, new_location)


def update_user_public_status(email: str, new_status: str):
    """
    This is used for updating a user's status.

    :param email: The email used to identify the user.
    :param new_status: The status to update.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    update_user_public_status_db(session, user.id, new_status)


def update_user_blocked_status(email: str, blocked: bool):
    """
    This is used for updating a user's blocked status.

    :param email: The email used to identify the user.
    :param blocked: The blocked status to update.
    """
    user = get_user_by_mail_db(session, email)
    if user is None:
        raise KeyError()
    update_user_blocked_status_db(session, user.id, blocked)


def set_user_interests(user_id: int, interests: list):
    """
    This function is used for setting a user's interests.

    :param user_id: The id of the user you want to set the interests.
    :param interests: The interests to set in a list.
    """
    delete_user_interests(session, user_id)
    for interest in interests:
        add_user_interest(session, user_id, interest)


def get_user_interests(user_id: int):
    """
    This function is used for getting a user's interests.

    :param user_id: The id of the user you want the interests.
    :return: A list of the user's interests.
    """
    return get_user_interests_db(session, user_id)


def search_for_users(
    username: str, start: int, amount: int, email=None, in_followers=False
):
    """
    This function is used for searching for users.
    It only lists users that are not admins.

    :param username: The username to search for.
    :param start: The start of the search. (offset)
    :param amount: The amount of users to return.
    :return: A list of users.
    """
    if in_followers:
        return search_users_in_followers_db(session, username, start, amount, email)
    return search_for_users_db(session, username, start, amount)


def search_for_users_admins(username: str, start: int, amount: int):
    """
    This function is used for searching for users.
    Lists all users, including those who are admins.

    :param username: The username to search for.
    :param start: The start of the search. (offset)
    :param amount: The amount of users to return.
    :return: A list of users.
    """
    return search_for_users_admins_db(session, username, start, amount)


session.close()
