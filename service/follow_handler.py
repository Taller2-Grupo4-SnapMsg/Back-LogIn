# follow_handler.py
"""
This module is used to encapsulate all the following and followers related functions.
"""
from repository.errors import RelationAlreadyExists
from repository.user_repository import (
    get_user_email,
    is_following as is_following_repo,
    is_follower as is_follower_repo,
    get_followers_count as get_followers_count_repo,
    get_following_count as get_following_count_repo,
    get_following_relations as get_following_relations_repo,
    get_followers as get_followers_repo,
    get_following as get_following_repo,
    create_follow as create_follow_repo,
    remove_follow as remove_follow_repo,
)
from service.errors import (
    UserNotFound,
    FollowingRelationAlreadyExists,
    UserCantFollowItself,
)


class FollowHandler:
    """
    Class used to encapsulate all the following and followers related functions.
    """

    def create_follow(self, email: str, email_to_follow: str):
        """
        This function is used to create a follow relationship.
        """
        if email == email_to_follow:
            raise UserCantFollowItself()
        try:
            create_follow_repo(email, email_to_follow)
        except KeyError as error:
            raise UserNotFound() from error
        except RelationAlreadyExists as error:
            raise FollowingRelationAlreadyExists() from error

    def get_all_followers(self, email: str):
        """
        This function is used to retrieve all username's followers from the database.
        """
        try:
            user = get_user_email(email)
            return get_followers_repo(user.id)
        except KeyError as error:
            raise UserNotFound() from error

    def get_all_following(self, email: str):
        """
        This function is used to retrieve all users following  username from the database.
        """
        try:
            user = get_user_email(email)
            return get_following_repo(user.id)
        except KeyError as error:
            raise UserNotFound() from error

    def get_all_following_relations(self):
        """
        This function is used to retrieve all follow relations from the database.
        """
        return get_following_relations_repo()

    def get_following_count(self, email: str):
        """
        This function is used to get email's following count from database.
        """
        try:
            user = get_user_email(email)
            return get_following_count_repo(user.id)
        except KeyError as error:
            raise UserNotFound() from error

    def get_followers_count(self, email: str):
        """
        This function is used to get email's followers count from database.
        """
        try:
            user = get_user_email(email)
            return get_followers_count_repo(user.id)
        except KeyError as error:
            raise UserNotFound() from error

    def remove_follow(self, email: str, email_to_unfollow: str):
        """
        This function is used to remove a follow relationship.
        """
        try:
            user = get_user_email(email)
            user_to_unfollow = get_user_email(email_to_unfollow)
            remove_follow_repo(user.id, user_to_unfollow.id)
            return {"message": "Unfollow successful"}
        except KeyError as error:
            raise UserNotFound() from error

    def is_following(self, email: str, email_to_check_if_following: str):
        """
        This function is used to check if a user is following another user.
        """
        try:
            user = get_user_email(email)
            user_to_check = get_user_email(email_to_check_if_following)
            return is_following_repo(user.id, user_to_check.id)
        except KeyError as error:
            raise UserNotFound() from error

    def is_follower(self, email: str, email_to_check_if_follower: str):
        """
        This function is used to check if a user is a follower of another user.
        """
        try:
            user = get_user_email(email)
            user_to_check = get_user_email(email_to_check_if_follower)
            return is_follower_repo(user.id, user_to_check.id)
        except KeyError as error:
            raise UserNotFound() from error
