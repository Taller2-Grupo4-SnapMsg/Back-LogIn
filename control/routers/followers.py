# followers.py
"""
All of the user's followers and following are managed here.
"""
from fastapi import (
    APIRouter,
    Header,
    HTTPException,
)

from service.follow_handler import FollowHandler

from service.errors import (
    UserNotFound,
    UserCantFollowItself,
    FollowingRelationAlreadyExists,
)

from control.utils.utils import (
    check_and_get_user_from_token,
    generate_response_list,
)

from control.codes import (
    USER_NOT_FOUND,
)

# Singleton instance of the AuthHandler class:
from control.utils.auth import auth_handler

router = APIRouter(tags=["Followers"])
origins = ["*"]

handler = FollowHandler()


@router.post("/follow/{email_following}")
def create_follow(email_following: str, token: str = Header(...)):
    """
    This function creates a following relation between the given users.

    :param token: Identifier of the user who wants to follow someone.
    :param email_following: Email of the user that is going to be followed.
    :return: Status code with a JSON message.
    """
    try:
        user_follower = check_and_get_user_from_token(token)
        handler.create_follow(user_follower.email, email_following)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    except UserCantFollowItself as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except FollowingRelationAlreadyExists as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"message": "Follow successful"}


@router.get("/followers/{email}")
def get_followers(email: str, token: str = Header(...)):
    """
    This function returns the users a username is followed by.

    :param email: Email of the user to get the followers of.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    check_and_get_user_from_token(token)
    try:
        user_list = handler.get_all_followers(email)
        return generate_response_list(user_list)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.get("/is_following/{email}")
def get_is_following(email_following: str, token: str = Header(...)):
    """
    This function returns if the user is following the given user.

    :param email: Email of the user to check if is following.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """

    email_follower = auth_handler.decode_token(token)
    check_and_get_user_from_token(token)
    try:
        return handler.is_following(email_follower, email_following)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.get("/is_follower/{email}")
def get_is_follower(email_follower: str, token: str = Header(...)):
    """
    This function returns if the user is a follower the given user.

    :param email: Email of the user to check if is a follower.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    email = auth_handler.decode_token(token)
    check_and_get_user_from_token(token)
    try:
        return handler.is_follower(email, email_follower)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.get("/following/{email}")
def get_following(email: str, token: str = Header(...)):
    """
    This function returns the users a username is following.

    :param email: Email of the user to get the following of.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    # Checks the person requesting is a logged user:
    check_and_get_user_from_token(token)
    # Does the actual request:
    try:
        user_list = handler.get_all_following(email)
        return generate_response_list(user_list)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.get("/follow/{email}/count")
def get_followers_count(email: str, token: str = Header(...)):
    """
    This function returns the number of followers of a username.

    :param email: Email of the user to get the followers count of.
    :return: Status code with a JSON message.
    """
    # Checks the person requesting is a logged user:
    check_and_get_user_from_token(token)
    # Does the actual request:
    try:
        return handler.get_followers_count(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.get("/following/{email}/count")
def get_following_count(email: str, token: str = Header(...)):
    """
    This function returns the number of users a email is following.

    :param email: Email of the user to get the following count of.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    # Checks the person requesting is a logged user:
    check_and_get_user_from_token(token)
    # Does the actual request:
    try:
        return handler.get_following_count(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.delete("/unfollow")
def unfollow(email_unfollowing: str, token: str = Header(...)):
    """
    This function deletes a following relation between the given users.

    :param token: Identifier of the user that is going to unfollow someone.
    :param username_following: Username of the user that is going to be unfollowed.
    :return: Status code with a JSON message.
    """
    try:
        email_follower = auth_handler.decode_token(token)
        return handler.remove_follow(email_follower, email_unfollowing)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
