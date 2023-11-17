# codes.py
"""
This module is dedicated for all te response codes the API will return.
"""
from fastapi import status

OK = status.HTTP_200_OK
USER_ALREADY_REGISTERED = status.HTTP_409_CONFLICT
USER_NOT_FOUND = status.HTTP_404_NOT_FOUND
USER_NOT_ADMIN = status.HTTP_400_BAD_REQUEST
INCORRECT_CREDENTIALS = status.HTTP_401_UNAUTHORIZED
BLOCKED_USER = status.HTTP_403_FORBIDDEN
BAD_REQUEST = status.HTTP_400_BAD_REQUEST
