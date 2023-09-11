# controler.py

"""
This is the controller layer of the REST API for the login backend.
"""

from pydantic import BaseModel

# Para permitir pegarle a la API desde localhost:
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from service.user import User
from service.user import change_password as change_password_service
from service.user import get_user_email as get_user_service
from service.user import try_login
from service.user import remove_user_email
from service.user import get_all_users as get_all_users_service
from service.user import get_user_nickname
from service.errors import UserAlreadyRegistered, UserNotFound, PasswordDoesntMatch


app = FastAPI()

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
    nickname: str


# Create a POST route
@app.post("/register")
async def register_user(user_data: UserRegistration):
    """
    This function is the endpoint for user registration.
    """
    user = User()
    user.set_email(user_data.email)
    user.set_password(user_data.password)
    user.set_name(user_data.name)
    user.set_surname(user_data.last_name)
    user.set_nickname(user_data.nickname)
    user.set_bio("")
    user.set_date_of_birth("")

    try:
        user.save()
    except UserAlreadyRegistered as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {"message": "Registration successful"}


class UserLogIn(BaseModel):
    """
    This class is a Pydantic model for the request body.
    """

    email: str
    password: str


# Route to handle user login
@app.post("/login/")
def login(user_data: UserLogIn):
    """
    This function is a test function that mocks user login.

    :param user: The user to login.
    :return: Status code with a JSON message.
    """
    try:
        try_login(user_data.email, user_data.password)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except PasswordDoesntMatch as error:
        raise HTTPException(status_code=401, detail=str(error)) from error
    return {"message": "Login successful"}


# Route to get user details
@app.get("/users/{email}")
def get_user(email: str):
    """
    This function is a test function that mocks retrieving a user.

    :param email: The email of the user to get.
    :return: User details or a 404 response.
    """
    try:
        user = get_user_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return user


# Route to get user by username
@app.get("/users/{username}")
def get_user_by_username(username: str):
    """
    This function retrieves an user.

    :param username: The username of the user to get.
    :return: User details or a 404 response.
    """
    try:
        user = get_user_nickname(username)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
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
        raise HTTPException(status_code=404, detail=str(error)) from error
    return {"message": "User information updated"}


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
        raise HTTPException(status_code=404, detail=str(error)) from error
    return {"message": "User deleted"}


@app.get("/users/")
def get_all_users():
    """
    This function is a test function that mocks retrieving all users.

    :return: Status code with a JSON message.
    """
    get_all_users_service()
    return {"message": "All users retrieved"}


@app.get("/ping")
def ping():
    """
    This function is a test function that mocks a ping.

    :return: Status code with a JSON message.
    """
    return {"message": "pong"}
