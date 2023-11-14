# admins.py
"""
This module is dedicated for all the admin routes.
"""
from datetime import datetime, timedelta
from fastapi import (
    APIRouter,
    Header,
    HTTPException,
    Query,
)
from firebase_admin import storage

from service.follow_handler import FollowHandler
from service.admin_handler import AdminHandler
from service.user_handler import UserHandler
from service.errors import UserNotFound, MaxAmmountExceeded

from control.models.models import (
    UserResponse,
)
from control.utils.utils import (
    generate_response_list,
    token_is_admin,
    generate_response,
)
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


@router.get("/users/admin/find", response_model=UserResponse)
def get_user(
    email: str = Query(None, title="Email", description="User email"),
    username: str = Query(None, title="Username", description="Username of the user"),
    token: str = Header(...),
):
    """
    This function retrieves a user by either email or username.

    :param email: The email of the user to get.
    :param username: The username of the user to get.
    :param token: Token used to verify the user.
    :return: User details or a 404 response.
    """
    # Checks the person requesting is a logged user:
    if not token_is_admin(token):
        raise HTTPException(
            status_code=USER_NOT_ADMIN,
            detail="Only administrators can use this endpoint",
        )

    if email is None and username is None:
        raise HTTPException(
            status_code=400,
            detail="At least one of 'email' or 'username' must be provided.",
        )

    if email:
        try:
            user = user_handler.get_user_email(email)
            user = generate_response(user)
            return user
        except UserNotFound as error:
            raise HTTPException(
                status_code=USER_NOT_FOUND, detail=str(error)
            ) from error

    if username:
        try:
            user = user_handler.get_user_username(username)
            user = generate_response(user)
            return user
        except UserNotFound as error:
            raise HTTPException(
                status_code=USER_NOT_FOUND, detail=str(error)
            ) from error
    # it never reachs here, but pylint...
    return {"message": "Something went wrong"}


@router.get("/users/admin/image")
def translate_path_to_image_link(firebase_path: str, token: str = Header(...)):
    """
    This endpoint translates the image_path from firebase to
    a normal link that can be displayed in the browser.

    :param firebase_path: The path to the image in firebase.
    :param token: Token used to verify the admin.

    :return: A link to the image.
    """
    if not token_is_admin(token):
        raise HTTPException(
            status_code=USER_NOT_ADMIN,
            detail="Incorrect Credentials",
        )
    # Replace "%2F" with / and %40 with @
    firebase_path = firebase_path.replace("%2F", "/").replace("%40", "@")
    bucket = storage.bucket()
    blob = bucket.blob(firebase_path)
    expiration_time = datetime.utcnow() + timedelta(minutes=5)
    url = blob.generate_signed_url(expiration=expiration_time, method="GET")
    return {"detail": url}


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
