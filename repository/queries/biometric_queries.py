# user_queries.py
"""
Module dedicated to the queries that the repository might need.
"""
from sqlalchemy.exc import IntegrityError
from repository.tables.users import BiometricToken

def add_user_biometric_token(session, user_id, biometric_token):
    """
    Adds a biometric token to the user.
    """
    try:
        new_biometric_token = BiometricToken(user_id, biometric_token)
        session.add(new_biometric_token)
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise error


def get_biometric_token(session, biometric_token_to_check):
    """
    Gets an user_id from a biometric token.
    """
    user_id = (
        session.query(BiometricToken.user_id)
        .filter_by(biometric_token=biometric_token_to_check.strip())
        .scalar()
    )
    if user_id is None:
        return None
    return user_id


def remove_biometric_token(session, user_id, user_biometric_token):
    """
    Removes a biometric token from the user.
    """
    try:
        session.query(BiometricToken).filter_by(
            user_id=user_id, biometric_token=user_biometric_token
        ).delete()
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise error
