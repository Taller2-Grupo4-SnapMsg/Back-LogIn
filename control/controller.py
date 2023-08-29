"""
This is the controller layer of the REST API for the login backend.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

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
    rn: int = random.randint(0, limit)
    return {'random': rn, 'limit': limit}

# Mock database to store user information
mock_db = {}

# Pydantic model for user registration
class UserRegistration(BaseModel):
    email: str
    password: str

# Pydantic model for updating user information
class UpdateUser(BaseModel):
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
