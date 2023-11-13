# admins.py
"""
This module is dedicated for all the admin routes.
"""
from fastapi import (
    APIRouter,
    Header,
    HTTPException,
    Query,
)

from service.follow_handler import FollowHandler
from service.admin_handler import AdminHandler
from service.user_handler import UserHandler
from service.errors import UserNotFound, MaxAmmountExceeded

from control.models.models import (
    UserResponse,
)
from control.utils.utils import generate_response_list, token_is_admin
from control.codes import (
    USER_NOT_FOUND,
    USER_NOT_ADMIN,
    BAD_REQUEST,
)

router = APIRouter(
    tags=["Admins"],
)
origins = ["*"]

# We create global handlers for the service layer.
# Since the handlers are stateless, we don't care if it's global.
follower_handler = FollowHandler()
admin_handler = AdminHandler()
user_handler = UserHandler()


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
def get_all_users(
    start: int = Query(0, title="offset", description="offset for pagination"),
    ammount: int = Query(
        10, title="ammount", description="max ammount of users to return"
    ),
    token: str = Header(...),
):
    """
    This function is a functon that returns all of the users in the database.

    :param start: The offset for pagination.
    :param ammount: The max ammount of users to return.
    :param token: Token used to verify the user who is calling this is an admin.

    :return: JSON of all users.
    """
    if not token_is_admin(token):
        raise HTTPException(
            status_code=USER_NOT_ADMIN,
            detail="Only administrators can get all users",
        )
    try:
        user_list = admin_handler.get_all_users(start, ammount)
    except ValueError as error:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(error)) from error
    except MaxAmmountExceeded as error:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(error)) from error
    return generate_response_list(user_list)


@router.get("/users/{query}")
def get_users_by_query(
    query: str,
    start: int = Query(0, title="offset", description="offset for pagination"),
    ammount: int = Query(
        10, title="ammount", description="max ammount of users to return"
    ),
    token: str = Header(...),
):
    """
    Function for admins so they can search by a query

    :param query: The query to search by
    :param start: The offset for pagination.
    :param ammount: The max ammount of users to return.
    """
    if not token_is_admin(token):
        raise HTTPException(
            status_code=USER_NOT_ADMIN,
            detail="Incorrect credentials",
        )
    try:
        options = {
            "start": start,
            "ammount": ammount,
            "in_followers": False,
            "email": None,
        }
        user_list = user_handler.search_for_users(query, options)
    except MaxAmmountExceeded as error:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(error)) from error
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
