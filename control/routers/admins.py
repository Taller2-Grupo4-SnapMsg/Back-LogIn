# admins.py
"""
This module is dedicated for all the admin routes.
"""
from fastapi import (
    APIRouter,
    Header,
    HTTPException,
)

from service.follow_handler import FollowHandler
from service.admin_handler import AdminHandler
from service.errors import UserNotFound

from control.models.models import (
    UserResponse,
)
from control.utils.utils import generate_response_list, token_is_admin
from control.codes import (
    USER_NOT_FOUND,
    USER_NOT_ADMIN,
)

router = APIRouter(
    tags=["Admins"],
)
origins = ["*"]

# We create global handlers for the service layer.
# Since the handlers are stateless, we don't care if it's global.
follower_handler = FollowHandler()
admin_handler = AdminHandler()


@router.put("/users/block/{email}")
def set_blocked_status(email: str, blocked: bool, token: str = Header(...)):
    """
    This function is for changing a user's blocked status.

    :param email: Email of the user to block.
    :param blocked: New blocked status.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        if not token_is_admin(token):
            raise HTTPException(
                status_code=USER_NOT_ADMIN,
                detail="Only administrators can change a user's blocked status",
            )
        admin_handler.change_blocked_status(email, blocked)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": email + " is now " + ("blocked" if blocked else "unblocked")}


@router.get(
    "/users",
    responses={
        200: {"model": UserResponse, "description": "All users"},
        400: {"description": "Only administrators can get all users"},
    },
)
def get_all_users(token: str = Header(...)):
    """
    This function is a functon that returns all of the users in the database.

    :param token: Token used to verify the user who is calling this is an admin.

    :return: JSON of all users.
    """
    if not token_is_admin(token):
        raise HTTPException(
            status_code=USER_NOT_ADMIN,
            detail="Only administrators can get all users",
        )
    user_list = admin_handler.get_all_users()
    return generate_response_list(user_list)


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
    return follower_handler.get_all_following_relations()
