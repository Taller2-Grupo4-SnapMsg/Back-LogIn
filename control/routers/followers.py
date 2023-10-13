# followers.py
"""
All of the user's followers and following are managed here.
"""
from fastapi import (
    APIRouter,
    Header,
    HTTPException,
)

from service.user import (
    create_follow as create_follow_service,
    get_all_following_relations as get_all_following_relations_service,
    get_all_followers,
    get_all_following,
    get_followers_count as get_followers_count_service,
    get_following_count as get_following_count_service,
    remove_follow as remove_follow_service,
    is_following as is_following_service,
    is_follower as is_follower_service,
)

from service.errors import (
    UserNotFound,
    UserCantFollowItself,
    FollowingRelationAlreadyExists,
)

from control.utils.utils import (
    check_for_user_token,
    generate_response_list,
    token_is_admin,
)

from control.codes import (
    USER_NOT_FOUND,
    USER_NOT_ADMIN,
)

# Singleton instance of the AuthHandler class:
from control.utils.auth import auth_handler

router = APIRouter(tags=["Followers"])
origins = ["*"]


@router.post("/follow")
def create_follow(email_following: str, token: str = Header(...)):
    """
    This function creates a following relation between the given users.

    :param token: Identifier of the user who wants to follow someone.
    :param email_following: Email of the user that is going to be followed.
    :return: Status code with a JSON message.
    """
    try:
        email_follower = auth_handler.decode_token(token)
        create_follow_service(email_follower, email_following)
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
    check_for_user_token(token)
    try:
        user_list = get_all_followers(email)
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
    check_for_user_token(token)
    try:
        return is_following_service(email_follower, email_following)
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
    check_for_user_token(token)
    try:
        return is_follower_service(email, email_follower)
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
    check_for_user_token(token)
    # Does the actual request:
    try:
        user_list = get_all_following(email)
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
    check_for_user_token(token)
    # Does the actual request:
    try:
        return get_followers_count_service(email)
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
    check_for_user_token(token)
    # Does the actual request:
    try:
        return get_following_count_service(email)
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
        return remove_follow_service(email_follower, email_unfollowing)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.get("/following")
def get_all_following_relations(token: str = Header(...)):
    """
    This function is a function that returns all of the following relations in the database.

    :param token: Token used to verify the user who is calling this is an admin.

    :return: JSON of all users.
    """
    if not token_is_admin(token):
        raise HTTPException(
            status_code=USER_NOT_ADMIN,
            detail="Only administrators can get all following relations",
        )
    return get_all_following_relations_service()
