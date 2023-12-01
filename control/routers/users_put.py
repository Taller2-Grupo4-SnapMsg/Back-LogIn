# users_put.py
"""
This module is for all the put methods of the users.
"""
from datetime import datetime
from fastapi import (
    APIRouter,
    Header,
    HTTPException,
)
from service.user_handler import UserHandler
from service.errors import (
    UserNotFound,
)

# Singleton instance of the AuthHandler class:
from control.utils.auth import auth_handler
from control.codes import (
    USER_NOT_FOUND,
)
from control.utils.utils import check_and_get_user_from_token, push_metric
from control.utils.tracer import tracer
from control.utils.logger import logger

from control.utils.metrics import GeoZoneMetric

router = APIRouter(tags=["Users"])
origins = ["*"]

# We create a global handler for the service layer.
# Since the handler is stateless, we don't care if it's global.
user_handler = UserHandler()


# Route to update user information
@router.put("/users/password")
@tracer.start_as_current_span("Change Password")
def change_password(new_password: str, token: str = Header(...)):
    """
    This function is for changing the user's password

    :param email: The email of the user to update.
    :param new_password: User's new password.
    :return: Status code with a JSON message.
    """
    try:
        user = check_and_get_user_from_token(token)
        new_password = auth_handler.get_password_hash(new_password)
        user_handler.change_password(user.email, new_password)
        logger.info("User %s changed password", user.email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/bio")
@tracer.start_as_current_span("Change Bio")
def change_bio(new_bio: str, token: str = Header(...)):
    """
    This function is for changing the user's bio

    :param new_bio: User's new bio.
    :param token: Token used to identify the user.
    :return: Status code with a JSON message.
    """
    try:
        user = check_and_get_user_from_token(token)
        user_handler.change_bio(user.email, new_bio)
        logger.info("User %s changed bio to %s from %s", user.email, new_bio, user.bio)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/avatar")
@tracer.start_as_current_span("Change Avatar")
def change_avatar(new_avatar: str, token: str = Header(...)):
    """
    This function is for changing the user's avatar

    :param new_avatar: User's new avatar.
    :param token: Token used to identify the user.
    :return: Status code with a JSON message.
    """
    try:
        user = check_and_get_user_from_token(token)
        user_handler.change_avatar(user.email, new_avatar)
        logger.info("User %s changed avatar", user.email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/name")
@tracer.start_as_current_span("Change Name")
def change_name(new_name: str, token: str = Header(...)):
    """
    This function is for changing the user's name

    :param new_name: User's new name.
    :param token: Token used to identify the user.
    :return: Status code with a JSON message.
    """
    try:
        user = check_and_get_user_from_token(token)
        user_handler.change_name(user.email, new_name)
        logger.info(
            "User %s changed name to %s from %s", user.email, new_name, user.name
        )
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/date_of_birth")
@tracer.start_as_current_span("Change Date of Birth")
def change_date_of_birth(new_date_of_birth: str, token: str = Header(...)):
    """
    This function is for changing the user's date_of_birth

    :param new_date_of_birth: User's new date_of_birth.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        user = check_and_get_user_from_token(token)
        user_handler.change_date_of_birth(user.email, new_date_of_birth)
        logger.info(
            "User %s changed date of birth to %s from %s",
            user.email,
            new_date_of_birth,
            user.date_of_birth,
        )
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/last_name")
@tracer.start_as_current_span("Change Last Name")
def change_last_name(new_last_name: str, token: str = Header(...)):
    """
    This function is for changing the user's last_name

    :param new_last_name: User's new last_name.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        user = check_and_get_user_from_token(token)
        user_handler.change_last_name(user.email, new_last_name)
        logger.info(
            "User %s changed last name to %s from %s",
            user.email,
            new_last_name,
            user.surname,
        )
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/location")
@tracer.start_as_current_span("Change Location")
def change_location(new_location: str, token: str = Header(...)):
    """
    This function is for changing the user's location

    :param new_location: User's new location.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        geozone_metric = GeoZoneMetric(datetime.now())
        user = check_and_get_user_from_token(token)
        geozone_metric.set_old_location(user.location)
        user_handler.change_location(user.email, new_location)
        geozone_json = (
            geozone_metric.set_timestamp_finish(datetime.now())
            .set_user_email(user.email)
            .set_new_location(new_location)
            .to_json()
        )
        push_metric(geozone_json)
        logger.info(
            "User %s changed location to %s from %s",
            user.email,
            new_location,
            user.location,
        )
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/interests")
@tracer.start_as_current_span("Change Interests")
def change_interests(new_interests: str, token: str = Header(...)):
    """
    This function is for changing the user's interests

    :param new_interests: User's new interests.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        user = check_and_get_user_from_token(token)
        user_handler.set_user_interests(user.email, new_interests)
        logger.info("User %s changed their interests to %s", user.email, new_interests)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@router.put("/users/privacy")
@tracer.start_as_current_span("Change Privacy")
def change_user_privacy(is_public: bool, token: str = Header(...)):
    """
    This function is for changing the user's privacy

    :param is_public: User's new privacy.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        user = check_and_get_user_from_token(token)
        user_handler.change_public_status(user.email, is_public)
        logger.info(
            "User %s changed privacy to %s from %s",
            user.email,
            is_public,
            user.is_public,
        )
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User privacy updated, now profle is public: " + str(is_public)}
