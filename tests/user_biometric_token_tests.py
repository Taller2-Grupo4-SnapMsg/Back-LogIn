"""
This module contains tests for the user biometric token.
"""

import pytest
from service.user_handler import UserHandler
from tests.utils import remove_test_user_from_db, save_test_user_to_db, EMAIL
from service.errors import UserNotFound

# We create the handler that will be used in all tests.
# Since the handler is stateless, we don't care if it's global.
handler = UserHandler()

def test_user_biometric_token():
    """
    This test checks that the user biometric token is correctly set.
    """
    remove_test_user_from_db()
    save_test_user_to_db()
    handler.add_biometric_token(EMAIL, "token")
    user = handler.verify_biometric_token("token")
    assert user.email == EMAIL
    remove_test_user_from_db()

def test_user_biometric_token_wrong_token():
    """
    This test checks that the user biometric token is correctly set.
    """
    remove_test_user_from_db()
    save_test_user_to_db()
    with pytest.raises(UserNotFound) as error:
        handler.verify_biometric_token("token")
    assert str(error.value) == "User not found"
    remove_test_user_from_db()
