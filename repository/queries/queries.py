# queries.py
"""
Module dedicated to the queries that the repository might need.
"""
from sqlalchemy.exc import IntegrityError
from repository.tables.users import User
from repository.errors import UsernameAlreadyExists, EmailAlreadyExists


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
        snaps=data["snaps"],
        followers=data["followers"],
        following=data["following"],
        avatar=data["avatar"],
        bio=data["bio"],
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
        setattr(user, "password", new_password)
        session.commit()
        return user
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
        session.delete(user)
        session.commit()
        return True
    return False


# to do: maybe delete this?
def get_id_by_username(session, username):
    """
    Queries the database for the id of the user with the given username.
    """
    return session.query(User).filter(User.username == username).first().id


def get_all_users(session):
    """
    Query mostly for testing, it retrieves all the users of the database.
    """
    return session.query(User).all()
