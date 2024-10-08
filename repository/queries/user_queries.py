# user_queries.py
"""
Module dedicated to the queries that the repository might need.
"""
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from repository.tables.users import User, Interests, Following
from repository.errors import (
    UsernameAlreadyExists,
    EmailAlreadyExists,
    InterestAlreadyExists,
)


def get_user_by_id(session, user_id):
    """
    Searches for a user by its id.
    """
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_username(session, username):
    """
    Searches for a user by its username.
    """
    return session.query(User).filter(User.username == username).first()


def get_user_by_mail(session, mail):
    """
    Searches for a user by its mail.
    """
    return session.query(User).filter(User.email == mail).first()


def create_user(session, email, password, username, data):
    """
    Inserts a new user to the users table.
    :param: session: the session to use
    :param: username: the username of the user
    :param: surname: the surname of the user
    :param: name: the name of the user
    :param: password: the password of the user (already hashed)
    :param: email: the email of the user
    :param: date_of_birth: the date of birth of the user
    :returns: the user created or None if it fails
    """
    user = User(
        username=username,
        surname=data["surname"],
        name=data["name"],
        password=password,
        email=email,
        date_of_birth=data["date_of_birth"],
        bio=data["bio"],
        avatar=data["avatar"],
        location=data["location"],
        blocked=data["blocked"],
        is_public=data["is_public"],
    )
    try:
        session.add(user)
        session.commit()
        return user
    except IntegrityError as error:
        session.rollback()
        if "username" in str(error.orig):
            raise UsernameAlreadyExists() from error
        # if it's not the username, it's the email, there is no other unique fields
        raise EmailAlreadyExists() from error


def update_user_password(session, user_id, new_password):
    """
    Changes the information of the user with new_data
    :param: session: the session to use
    :param: user_id: the id of the user to change
    :param: new_data: the new data to change
    :returns: the user updated or None if it fails
    """
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        try:
            setattr(user, "password", new_password)
            session.commit()
            return user
        except IntegrityError:
            session.rollback()
    return None


def delete_user(session, user_id):
    """
    Deletes the user with the given id.
    :param: session: the session to use
    :param: user_id: the id of the user to delete
    :returns: True if it found and deleted the user, false if it didn't
    """
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        try:
            session.delete(user)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
    return False


# to do: maybe delete this?
def get_id_by_username(session, username):
    """
    Queries the database for the id of the user with the given username.
    """
    return session.query(User).filter(User.username == username).first().id


def update_user_bio(session, user_id, new_bio):
    """
    Changes the bio of the user with the given id.
    """
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        try:
            setattr(user, "bio", new_bio)
            session.commit()
            return user
        except IntegrityError:
            session.rollback()
    return None


def update_user_name(session, user_id, new_name):
    """
    Changes the name of the user with the given id.
    """
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        try:
            setattr(user, "name", new_name)
            session.commit()
            return user
        except IntegrityError:
            session.rollback()
    return None


def update_user_date_of_birth(session, user_id, new_date_of_birth):
    """
    Changes the date_of_birth of the user with the given id.
    """
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        try:
            setattr(user, "date_of_birth", new_date_of_birth)
            session.commit()
            return user
        except IntegrityError:
            session.rollback()
    return None


def update_user_last_name(session, user_id, new_last_name):
    """
    Changes the last name of the user with the given id.
    """
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        try:
            setattr(user, "surname", new_last_name)
            session.commit()
            return user
        except IntegrityError:
            session.rollback()
    return None


def update_user_avatar(session, user_id, new_avatar):
    """
    Changes the avatar of the user with the given id.
    """
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        try:
            setattr(user, "avatar", new_avatar)
            session.commit()
            return user
        except IntegrityError:
            session.rollback()
    return None


def update_user_location(session, user_id, new_location):
    """
    Changes the location of the user with the given id.
    """
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        try:
            setattr(user, "location", new_location)
            session.commit()
            return user
        except IntegrityError:
            session.rollback()
    return None


def update_user_blocked_status(session, user_id, blocked):
    """
    Changes the blocked status of the user with the given id.
    """
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        try:
            setattr(user, "blocked", blocked)
            session.commit()
            return user
        except IntegrityError:
            session.rollback()
    return None


def update_user_public_status(session, user_id, public):
    """
    Changes the public status of the user with the given id.
    """
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        try:
            setattr(user, "is_public", public)
            session.commit()
            return user
        except IntegrityError:
            session.rollback()
    return None


def get_all_users(session, start, ammount):
    """
    Query mostly for testing, it retrieves all the users of the database.
    """
    return session.query(User).offset(start).limit(ammount).all()


def delete_user_interests(session, user_id):
    """
    Deletes all the interests of the user with the given id.

    :param: session: the session to use
    :param: user_id: the id of the user to delete
    :returns: True if it found and deleted the user's interests, false if it didn't.
    (False means the user didn't have any interests)
    """
    interests = session.query(Interests).filter(Interests.user_id == user_id).all()
    if interests:
        try:
            for interest in interests:
                session.delete(interest)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
    return False


def add_user_interest(session, user_id, interest):
    """
    Adds to the interests table a interest for given user_id

    :param: session: the session to use
    :param: user_id: the id of the user to add the interest
    :param: interest: the interest to add
    """
    interest = Interests(user_id=user_id, interest=interest)
    try:
        session.add(interest)
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise InterestAlreadyExists(
            f"Interest {interest} already exists for user"
        ) from error


def get_user_interests(session, user_id):
    """
    Gets all the interests of the user with the given id.

    :param: session: the session to use
    :param: user_id: the id of the user to get the interests
    :returns: a list of the interests of the user
    """
    return session.query(Interests).filter(Interests.user_id == user_id).all()


def search_for_users(session, query: str, start, amount):
    """
    Searches for users with the given username.

    :param: session: the session to use
    :param: query: the query to search for
    :param: start: the start of the search (offset)
    :param: amount: the amount of users to return
    :returns: a list of users with the given query
    """
    return (
        session.query(User)
        .filter(
            or_(
                User.email.ilike(f"%{query}%"),
                User.username.ilike(f"%{query}%"),
                User.name.ilike(f"%{query}%"),
                User.surname.ilike(f"%{query}%"),
            )
        )
        .offset(start)
        .limit(amount)
        .all()
    )


def search_users_in_followers(session, username: str, start, amount, email):
    """
    Searches for users with the given username.

    :param: session: the session to use
    :param: username: the username to search for
    :param: start: the start of the search (offset)
    :param: amount: the amount of users to return
    :returns: a list of users with the given username who are followed by others
    """
    user = session.query(User).filter(User.email == email).first()
    user_id = user.id
    return (
        session.query(User)
        .join(Following, Following.user_id == User.id)
        .filter(Following.following_id == user_id)
        .filter(User.username.ilike(f"{username}%"))
        .offset(start)
        .limit(amount)
    )
