# admins.py
"""
This module is dedicated for all the admin routes.
"""
from fastapi import (
    APIRouter,
    Header,
    HTTPException,
)
from service.user import (
    get_all_users as get_all_users_service,
    make_admin as make_admin_service,
    remove_admin_status as remove_admin_service,
    is_email_admin,
    change_blocked_status as change_blocked_status_service,
    search_for_users_admins,
    get_all_following_relations as get_all_following_relations_service,
)
from service.errors import UserNotFound

from control.models.models import (
    UserLogIn,
    UserRegistration,
    UserResponse,
)
from control.utils.utils import (
    generate_response_list,
    token_is_admin,
    create_user_from_user_data,
    handle_user_registration,
    handle_user_login,
    handle_get_user_email,
)
from control.utils.auth import auth_handler
from control.codes import (
    USER_NOT_FOUND,
    INCORRECT_CREDENTIALS,
    USER_NOT_ADMIN,
)

router = APIRouter(
    tags=["Admins"],
)
origins = ["*"]


@router.post("/register_admin")
def register_admin(user_data: UserRegistration):
    """
    This function is the endpoint for admin registration.
    """

    user = create_user_from_user_data(user_data)
    user.set_admin(True)
    return handle_user_registration(user)


@router.post("/login_admin", status_code=200, response_model=dict)
def login_admin(user_data: UserLogIn):
    """
    This function is the endpoint for the web backoffice front to log in an already existing admin

    :param user: The user to login.
    :return: Status code with a JSON message.
    """
    user = handle_get_user_email(user_data.email)
    if not user.admin:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        )
    return handle_user_login(user_data.password, user.password, user_data.email)


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
        admin_email = auth_handler.decode_token(token)
        if not is_email_admin(admin_email):
            raise HTTPException(
                status_code=USER_NOT_ADMIN,
                detail="Only administrators can block users",
            )
        change_blocked_status_service(email, blocked)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": email + " is now " + ("blocked" if blocked else "unblocked")}


# Route to making an admin
@router.put("/users/{email}/make_admin")
def make_admin(email: str, token: str = Header(...)):
    """
    This function changes the status of email to admin.

    :param email: The email of the user to update.
    :param token: Token used to verify the user who is calling this is an admin.
    :return: Status code with a JSON message.
    """
    if not token_is_admin(token):
        raise HTTPException(
            status_code=USER_NOT_ADMIN,
            detail="Only administrators can make other users administrators",
        )
    try:
        make_admin_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": email + " is now an admin"}


# Route to removing admin status
@router.put("/users/{email}/remove_admin")
def remove_admin_status(email: str, token: str = Header(...)):
    """
    This function is a test function that mocks updating user information.

    :param email: The email of the user to update.
    :param token: Token used to verify the user who is calling this is an admin.
    :return: Status code with a JSON message.
    """
    if not token_is_admin(token):
        raise HTTPException(
            status_code=USER_NOT_ADMIN,
            detail="Only administrators can remove other users from being administrators",
        )
    try:
        remove_admin_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": email + " is no longer an admin"}


@router.get("/admin/find_users/{username}")
def find_users(username: str, start: int, ammount: int, token: str = Header(...)):
    """
    Searches among all users (and admins) for a given username.

    :param username: The username to search for.
    :param start: The index of the first user to return.
    :param ammount: The ammount of users to return.
    :param token: Token used to verify the user who is calling this is an admin.
    :return: Status code with a JSON message.
    """
    if not token_is_admin(token):
        raise HTTPException(
            status_code=USER_NOT_ADMIN,
            detail="Only administrators can find users",
        )
    users = search_for_users_admins(username, start, ammount)
    return generate_response_list(users)


@router.get("/admin/is_admin")
def validate_admin_token(token: str = Header(...)):
    """
    This function checks if a token is an admin or not.

    :param token: The authentication token.
    :return: User details or a 401 response.
    """
    return {"is_admin": token_is_admin(token)}


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
    user_list = get_all_users_service()
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
    return get_all_following_relations_service()
