#controler.py

"""
This is the controller layer of the REST API for the login backend.
"""

import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/hello_world/")
def central_function():
    """
    This function is a test function.

    :return: Hello world.
    """
    return {"message": "Hello World"}


@app.get('/random/{limit}')
def get_random(limit: int):
    """
    This function is a test function that receives a parameter and returns
    a random number between 0 and the number given.

    :param limit: The limit of the random number.
    :return: Random number and limit.
    """
    random_number: int = random.randint(0, limit)
    return {'random': random_number, 'limit': limit}

# Mock database to store user information
mock_db = {}

# Pydantic model for user registration
# pylint: disable=too-few-public-methods
class UserRegistration(BaseModel):
    """
    Represents user registration data.

    This class defines the structure of user registration data,
    including the email and password fields.

    Attributes:
        email (str): The email address of the user.
        password (str): The user's chosen password.
    """
    email: str
    password: str

# Pydantic model for updating user information
# pylint: disable=too-few-public-methods
class UpdateUser(BaseModel):
    """
    Represents user update data.

    This class defines the structure of user update data,
    including the password field.

    Attributes:
        password (str): The user's newly chosen password.
    """
    password: str

# Route to handle user registration
@app.post("/register/")
def register(user: UserRegistration):
    """
    This function is a test function that mocks user registration.

    :param user: The user to register.
    :return: Status code with a JSON message.
    """
    if user.email in mock_db:
        raise HTTPException(status_code=400, detail="User already registered")
    mock_db[user.email] = {
        "email": user.email,
        "password": user.password
    }
    return {"message": "Registration successful"}

# Route to get user details
@app.get("/users/{email}/")
def get_user(email: str):
    """
    This function is a test function that mocks retrieving a user.

    :param email: The email of the user to get.
    :return: User details or a 404 response.
    """
    user = mock_db.get(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Route to update user information
@app.put("/users/{email}/")
def update_user(email: str, update_info: UpdateUser):
    """
    This function is a test function that mocks updating user information.

    :param email: The email of the user to update.
    :param update_info: New user information.
    :return: Status code with a JSON message.
    """
    user = mock_db.get(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user["password"] = update_info.password
    return {"message": "User information updated"}

@app.get("/ping")
def ping():
    """
    This function is a test function that mocks a ping.

    :return: Status code with a JSON message.
    """
    return {"message": "pong"}
