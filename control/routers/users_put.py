# users_put.py
"""
This module is for all the put methods of the users.
"""
from fastapi import (
    APIRouter,
    Header,
    HTTPException,
)
from service.user import (
    change_password as change_password_service,
    change_bio as change_bio_service,
    change_name as change_name_service,
    change_date_of_birth as change_date_of_birth_service,
    change_last_name as change_last_name_service,
    change_avatar as change_avatar_service,
    change_location as change_location_service,
    set_user_interests as change_interests_service,
    change_public_status,
)
from service.errors import (
    UserNotFound,
)

# Singleton instance of the AuthHandler class:
from control.utils.auth import auth_handler
from control.codes import (
    USER_NOT_FOUND,
)

router = APIRouter(tags=["Users"])
origins = ["*"]


# Route to update user information
@router.put("/users/password")
def change_password(new_password: str, token: str = Header(...)):
    """
    This function is for changing the user's password

    :param email: The email of the user to update.
    :param new_password: User's new password.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        new_password = auth_handler.get_password_hash(new_password)
        change_password_service(email, new_password)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/bio")
def change_bio(new_bio: str, token: str = Header(...)):
    """
    This function is for changing the user's bio

    :param new_bio: User's new bio.
    :param token: Token used to identify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_bio_service(email, new_bio)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/avatar")
def change_avatar(new_avatar: str, token: str = Header(...)):
    """
    This function is for changing the user's avatar

    :param new_avatar: User's new avatar.
    :param token: Token used to identify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_avatar_service(email, new_avatar)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/name")
def change_name(new_name: str, token: str = Header(...)):
    """
    This function is for changing the user's name

    :param new_name: User's new name.
    :param token: Token used to identify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_name_service(email, new_name)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/date_of_birth")
def change_date_of_birth(new_date_of_birth: str, token: str = Header(...)):
    """
    This function is for changing the user's date_of_birth

    :param new_date_of_birth: User's new date_of_birth.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_date_of_birth_service(email, new_date_of_birth)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/last_name")
def change_last_name(new_last_name: str, token: str = Header(...)):
    """
    This function is for changing the user's last_name

    :param new_last_name: User's new last_name.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_last_name_service(email, new_last_name)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/location")
def change_location(new_location: str, token: str = Header(...)):
    """
    This function is for changing the user's location

    :param new_location: User's new location.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_location_service(email, new_location)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/interests")
def change_interests(new_interests: str, token: str = Header(...)):
    """
    This function is for changing the user's interests

    :param new_interests: User's new interests.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_interests_service(email, new_interests)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/privacy")
def change_user_privacy(is_public: bool, token: str = Header(...)):
    """
    This function is for changing the user's privacy

    :param is_public: User's new privacy.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_public_status(email, is_public)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User privacy updated, now profle is public: " + str(is_public)}
