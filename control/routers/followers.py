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
from control.utils.tracer import tracer
from control.utils.logger import logger
from control.utils.utils import (
    check_and_get_user_from_token,
    generate_response_list,
)

from control.codes import (
    USER_NOT_FOUND,
)

router = APIRouter(tags=["Followers"])
origins = ["*"]

handler = FollowHandler()


@router.post("/follow/{email_following}")
@tracer.start_as_current_span("Create follow - Followers")
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
        logger.info("User %s followed user %s", user_follower.email, email_following)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    except UserCantFollowItself as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except FollowingRelationAlreadyExists as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"message": "Follow successful"}


@router.get("/followers/{email}")
@tracer.start_as_current_span("Get followers - Followers")
def get_followers(email: str, token: str = Header(...)):
    """
    This function returns the users a username is followed by.

    :param email: Email of the user to get the followers of.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    requester = check_and_get_user_from_token(token)
    try:
        user_list = handler.get_all_followers(email)
        logger.info("User %s got all the users following %s", requester.email, email)
        return generate_response_list(user_list)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.get("/is_following/{email}")
@tracer.start_as_current_span("Get is following - Followers")
def get_is_following(email_following: str, token: str = Header(...)):
    """
    This function returns if the user is following the given user.

    :param email: Email of the user to check if is following.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """

    user = check_and_get_user_from_token(token)
    try:
        logger.info("User %s asked if is following %s", user.email, email_following)
        return handler.is_following(user.email, email_following)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.get("/is_follower/{email}")
@tracer.start_as_current_span("Get is follower - Followers")
def get_is_follower(email_follower: str, token: str = Header(...)):
    """
    This function returns if the user is a follower the given user.

    :param email: Email of the user to check if is a follower.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    user = check_and_get_user_from_token(token)
    try:
        logger.info("User %s asked if is a follower of %s", user.email, email_follower)
        return handler.is_follower(user.email, email_follower)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.get("/following/{email}")
@tracer.start_as_current_span("Get following from email - Followers")
def get_following(email: str, token: str = Header(...)):
    """
    This function returns the users a username is following.

    :param email: Email of the user to get the following of.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    # Checks the person requesting is a logged user:
    requester = check_and_get_user_from_token(token)
    # Does the actual request:
    try:
        user_list = handler.get_all_following(email)
        logger.info("User %s got all the users %s is following", requester.email, email)
        return generate_response_list(user_list)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.get("/follow/{email}/count")
@tracer.start_as_current_span("Get follow count - Followers")
def get_followers_count(email: str, token: str = Header(...)):
    """
    This function returns the number of followers of a username.

    :param email: Email of the user to get the followers count of.
    :return: Status code with a JSON message.
    """
    # Checks the person requesting is a logged user:
    user = check_and_get_user_from_token(token)
    # Does the actual request:
    try:
        logger.info("User %s got the number of followers of %s", user.email, email)
        return handler.get_followers_count(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.get("/following/{email}/count")
@tracer.start_as_current_span("Get following count - Followers")
def get_following_count(email: str, token: str = Header(...)):
    """
    This function returns the number of users a email is following.

    :param email: Email of the user to get the following count of.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    # Checks the person requesting is a logged user:
    user = check_and_get_user_from_token(token)
    # Does the actual request:
    try:
        logger.info(
            "User %s got the number of users %s is following", user.email, email
        )
        return handler.get_following_count(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.delete("/unfollow")
@tracer.start_as_current_span("Delete follow - Followers")
def unfollow(email_unfollowing: str, token: str = Header(...)):
    """
    This function deletes a following relation between the given users.

    :param token: Identifier of the user that is going to unfollow someone.
    :param username_following: Username of the user that is going to be unfollowed.
    :return: Status code with a JSON message.
    """
    try:
        user = check_and_get_user_from_token(token)
        logger.info(
            "User %s is going to unfollow user %s", user.email, email_unfollowing
        )
        return handler.remove_follow(user.email, email_unfollowing)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
