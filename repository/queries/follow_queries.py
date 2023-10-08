# follow_queries.py
"""
Module dedicated to the queries that the repository might need for the following feature.
"""
from sqlalchemy.exc import IntegrityError
from repository.tables.users import User
from repository.tables.users import Following
from repository.queries.user_queries import get_user_by_mail
from repository.errors import RelationAlreadyExists


def create_follow(session, email, email_to_follow):
    """
    Creates a follow relationship between two users.
    """
    user = get_user_by_mail(session, email)
    user_to_follow = get_user_by_mail(session, email_to_follow)
    if user and user_to_follow:
        try:
            following = Following(user.id, user_to_follow.id)
            session.add(following)
            session.commit()
        except IntegrityError as error:
            session.rollback()
            raise RelationAlreadyExists() from error
        return following
    return None


def get_followers(session, user_id):
    """
    Returns a list of the followers of the user with the given username.
    """
    users = session.query(Following).filter(Following.following_id == user_id).all()
    return [
        session.query(User).filter(User.id == user.user_id).first() for user in users
    ]


def get_following(session, user_id):
    """
    Returns a list of the users that the user with the given username is following.
    """
    users = session.query(Following).filter(Following.user_id == user_id).all()
    return [
        session.query(User).filter(User.id == user.following_id).first()
        for user in users
    ]


def is_following(session, user_id, user_id_to_check_if_following):
    """
    Returns True if the user with the given id is following the user with the given id.
    """
    following = (
        session.query(Following)
        .filter(Following.user_id == user_id)
        .filter(Following.following_id == user_id_to_check_if_following)
        .first()
    )
    return following is not None


def get_following_relations(session):
    """
    Returns a list of all the following relations.
    """
    return session.query(Following).all()


def get_following_count(session, user_id):
    """
    Returns the number of users that the user with the given username is following.
    """
    return session.query(Following).filter(Following.user_id == user_id).count()


def get_followers_count(session, user_id):
    """
    Returns the number of followers of the user with the given username.
    """
    return session.query(Following).filter(Following.following_id == user_id).count()


def remove_follow(session, user_id, user_id_to_unfollow):
    """
    Removes the folowing relation between the two users.
    """
    following = (
        session.query(Following)
        .filter(Following.user_id == user_id)
        .filter(Following.following_id == user_id_to_unfollow)
        .first()
    )
    if following:
        session.delete(following)
        session.commit()
        return
    raise KeyError("The relation doesn't exist")
