# controler.py

"""
This is the controller layer of the REST API for the login backend.
"""
import datetime
from pydantic import BaseModel

# Para permitir pegarle a la API desde localhost:
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi import Depends
from service.user import User
from service.user import change_password as change_password_service
from service.user import get_user_email as get_user_service
from service.user import get_user_password
from service.user import remove_user_email
from service.user import get_all_users as get_all_users_service
from service.user import get_user_username
from service.user import make_admin as make_admin_service
from service.user import remove_admin_status as remove_admin_service
from service.errors import UserNotFound, PasswordDoesntMatch
from service.errors import UsernameAlreadyRegistered, EmailAlreadyRegistered
from control.auth import AuthHandler

USER_ALREADY_REGISTERED = 409
USER_NOT_FOUND = 404
PASSWORD_DOESNT_MATCH = 401

app = FastAPI()
auth_handler = AuthHandler()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define a Pydantic model for the request body
class UserRegistration(BaseModel):
    """
    This class is a Pydantic model for the request body.
    """

    password: str
    email: str
    name: str
    last_name: str
    username: str
    date_of_birth: str


# Create a POST route
@app.post("/register", status_code=201)
def register_user(user_data: UserRegistration):
    """
    This function is the endpoint for user registration.
    """

    user = User()

    hashed_password = auth_handler.get_password_hash(user_data.password)
    user.set_password(hashed_password)

    user.set_email(user_data.email)
    user.set_name(user_data.name)
    user.set_surname(user_data.last_name)
    user.set_username(user_data.username)
    user.set_bio("")
    date_time = user_data.date_of_birth.split(" ")
    user.set_date_of_birth(
        datetime.datetime(int(date_time[0]), int(date_time[1]), int(date_time[2]))
    )
    user.set_admin(False)
    try:
        user.save()
        token = auth_handler.encode_token(user_data.email)
    except UsernameAlreadyRegistered as error:
        raise HTTPException(
            status_code=USER_ALREADY_REGISTERED, detail=str(error)
        ) from error
    except EmailAlreadyRegistered as error:
        raise HTTPException(
            status_code=USER_ALREADY_REGISTERED, detail=str(error)
        ) from error
    return {"message": "Registration successful", "token": token}


class UserLogIn(BaseModel):
    """
    This class is a Pydantic model for the request body.
    """

    email: str
    password: str


# Route to handle user login
@app.post("/login/", status_code=200)
def login(user_data: UserLogIn):
    """
    This function is a test function that mocks user login.

    :param user: The user to login.
    :return: Status code with a JSON message.
    """
    try:
        # try_login(user_data.email, hash_password)
        hash_password = get_user_password(user_data.email)
        if auth_handler.verify_password(user_data.password, hash_password):
            # Passwords match, proceed with login
            token = auth_handler.encode_token(user_data.email)
            return {"message": "Login successful", "token": token}
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    except PasswordDoesntMatch as error:
        raise HTTPException(
            status_code=PASSWORD_DOESNT_MATCH, detail=str(error)
        ) from error
    # Excepcion token?
    return {
        "message": "Login unsuccessful, something went wrong, but we don't know what it is"
    }


@app.get("/protected")
def protected(useremail=Depends(auth_handler.auth_wrapper)):
    """
    Wrapper for protected routes.
    """
    return {"email": useremail}


# Route to get user details
@app.get("/users/email/{email}")
def get_user(email: str):
    """
    This function is a function that retrieves an user by mail.

    :param email: The email of the user to get.
    :return: User details or a 404 response.
    """
    try:
        user = get_user_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return user


# Route to get user by username
@app.get("/users/username/{username}")
def get_user_by_username(username: str):
    """
    This function retrieves an user by username.

    :param username: The username of the user to get.
    :return: User details or a 404 response.
    """
    try:
        user = get_user_username(username)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return user


# Route to update user information
@app.put("/users/{email}/")
def change_password(email: str, new_password: str):
    """
    This function is a test function that mocks updating user information.

    :param email: The email of the user to update.
    :param update_info: New user information.
    :return: Status code with a JSON message.
    """
    try:
        change_password_service(email, new_password)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


# Route to making an admin
@app.put("/users/{email}/make_admin")
def make_admin(email: str):
    """
    This function is a test function that mocks updating user information.

    :param email: The email of the user to update.
    :return: Status code with a JSON message.
    """
    try:
        make_admin_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": email + " is now an admin"}


# Route to removing admin status
@app.put("/users/{email}/remove_admin")
def remove_admin_status(email: str):
    """
    This function is a test function that mocks updating user information.

    :param email: The email of the user to update.
    :return: Status code with a JSON message.
    """
    try:
        remove_admin_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": email + " is no longer an admin"}


@app.delete("/users/{email}")
def delete_user(email: str):
    """
    This function is a test function that mocks deleting a user.

    :param email: The email of the user to delete.
    :return: Status code with a JSON message.
    """
    try:
        remove_user_email(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User deleted"}


@app.get("/users/")
def get_all_users():
    """
    This function is an auxiliary function that returns all the users in the db

    :return: JSON of all users.
    """
    return get_all_users_service()


@app.get("/ping")
def ping():
    """
    This function is a test function that mocks a ping.

    :return: Status code with a JSON message.
    """
    return {"message": "pong"}
