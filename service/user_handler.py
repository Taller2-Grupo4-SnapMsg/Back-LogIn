# user_handler.py
"""
This module encapsulates all the logic of the user's backend.
"""
from repository.user_repository import (
    update_user_password as update_user_password_repo,
    update_user_bio as update_user_bio_repo,
    update_user_name as update_user_name_repo,
    update_user_date_of_birth as update_user_date_of_birth_repo,
    update_user_last_name as update_user_last_name_repo,
    update_user_avatar as update_user_avatar_repo,
    get_user_email as get_user_repo,
    remove_user,
    get_user_username as get_user_username_repo,
    update_user_location as update_user_location_repo,
    set_user_interests as set_user_interests_repo,
    get_user_interests as get_user_interests_repo,
    search_for_users as search_for_users_repo,
    update_user_public_status as update_user_public_status_repo,
    add_user_biometric_token as add_user_biometric_token_repo,
    get_biometric_token as get_biometric_token_repo,
    remove_biometric_token as remove_biometric_token_repo,
)
from service.errors import (
    UserNotFound,
    PasswordDoesntMatch,
    MaxAmmountExceeded,
    UserAlreadyHasBiometricToken,
)
from repository.errors import RelationAlreadyExists

MAX_AMMOUNT = 25

class UserHandler:
    """
    This class encapsulates all the logic of the user's backend.
    """

    def try_login(self, email: str, password: str):
        """
        This function is used to login the user.

        :param email: The email of the user to login.
        :param password: The password of the user to login.
        """
        try:
            repo_user = get_user_repo(email)  # esto devuelve un usuario
            if repo_user.password != password:
                raise PasswordDoesntMatch()
        except KeyError as error:
            raise UserNotFound() from error
        return {"message": "Login successful"}

    def change_password(self, email: str, new_password: str):
        """
        This function is used to update the user in the database.

        :param email: The email of the user to update.
        :param new_passowrd: The user's new password.
        """
        try:
            update_user_password_repo(email, new_password)
        except KeyError as error:
            raise UserNotFound() from error

    def change_bio(self, email: str, new_bio: str):
        """
        This function is used to update the user in the database.

        :param email: The email of the user to update.
        :param new_bio: The user's new bio.
        """
        try:
            update_user_bio_repo(email, new_bio)
        except KeyError as error:
            raise UserNotFound() from error

    def change_name(self, email: str, new_name: str):
        """
        This function is used to update the user in the database.

        :param email: The email of the user to update.
        :param name: The user's new name.
        """
        try:
            update_user_name_repo(email, new_name)
        except KeyError as error:
            raise UserNotFound() from error

    def change_date_of_birth(self, email: str, new_date_of_birth: str):
        """
        This function is used to update the user in the database.

        :param email: The email of the user to update.
        :param new_date_of_birth: The user's new date of birth.
        """
        try:
            update_user_date_of_birth_repo(email, new_date_of_birth)
        except KeyError as error:
            raise UserNotFound() from error

    def change_last_name(self, email: str, new_last_name: str):
        """
        This function is used to update the user in the database.

        :param email: The email of the user to update.
        :param new_last_name: The user's new last name.
        """
        try:
            update_user_last_name_repo(email, new_last_name)
        except KeyError as error:
            raise UserNotFound() from error

    def change_avatar(self, email: str, new_avatar: str):
        """
        This function is used to update the user in the database.

        :param email: The email of the user to update.
        :param new_avatar: The user's new avatar.
        """
        try:
            update_user_avatar_repo(email, new_avatar)
        except KeyError as error:
            raise UserNotFound() from error

    def change_location(self, email: str, new_location: str):
        """
        This function is used to update the user in the database.

        :param email: The email of the user to update.
        :param new_location: The user's new location.
        """
        try:
            update_user_location_repo(email, new_location)
        except KeyError as error:
            raise UserNotFound() from error

    def change_public_status(self, email: str, public_status: bool):
        """
        This function is used to update the user in the database.

        :param email: The email of the user to update.
        :param public_status: The user's new public status.
        """
        try:
            update_user_public_status_repo(email, public_status)
        except KeyError as error:
            raise UserNotFound() from error

    def get_user_email(self, email: str):
        """
        This function is used to retrieve the user from the database.

        :param email: The email of the user to retrieve.
        :return: The user's information.
        """
        try:
            return get_user_repo(email)
        except KeyError as error:
            raise UserNotFound() from error

    def get_user_username(self, username: str):
        """
        This function is used to retrieve the user from the database.

        :param username: The username of the user to retrieve.
        :return: The user's information.
        """
        try:
            return get_user_username_repo(username)
        except KeyError as error:
            raise UserNotFound() from error

    def remove_user_email(self, email: str):
        """
        This function is used to remove the user from the database.

        :param email: The email of the user to remove.
        """
        try:
            remove_user(email)
        except KeyError as error:
            raise UserNotFound() from error

    def remove_user_username(self, username: str):
        """
        This function is used to remove the user from the database.

        :param username: The username of the user to remove.
        """

        user = self.get_user_username(username)
        remove_user(user.email)

    def set_user_interests(self, email: str, interests: str):
        """
        This function is used to set the user's interests.

        :param email: The email of the user to update.
        :param interests: The user's interests in a string format like "Coooking,Cars,planes".
        """

        user = self.get_user_email(email)
        interests_list = interests.split(",")
        set_user_interests_repo(user.id, interests_list)

    def get_user_interests(self, email: str):
        """
        This function is used to get the user's interests.

        :param email: The email of the user to update.
        :return: The user's interest in a list
        """
        user = self.get_user_email(email)
        interests = get_user_interests_repo(user.id)
        return [interest.interest for interest in interests]

    def search_for_users(self, username, options):
        """
        This function is used to search for users.

        :param username: The username of the user to search for.
        :param start: The start of the search (offset).
        :param ammount: The ammount of users to return. if it's greater than
        MAX_AMMOUNT, it will be set to MAX_AMMOUNT. And if there is not enough users
        it will return everything it found.
        :return: A list of users.
        """
        if options["ammount"] > MAX_AMMOUNT:
            raise MaxAmmountExceeded(
                "Ammount can't be greater than " + str(MAX_AMMOUNT)
            )
        return search_for_users_repo(
            username,
            options["start"],
            options["ammount"],
            options["email"],
            options["in_followers"],
        )

    def add_biometric_token(self, email: str, biometric_token: str):
        """
        This function is used to add a biometric token to the user.
        """
        try:
            # Here i should create the biometric_token, so i shouldnt receive it as a parameter
            add_user_biometric_token_repo(email, biometric_token)
        except KeyError as error:
            raise UserNotFound() from error
        except RelationAlreadyExists as error:
            raise UserAlreadyHasBiometricToken from error

    def verify_biometric_token(self, biometric_token: str):
        """
        This function is used to verify a biometric token of the user.
        """
        try:
            return get_biometric_token_repo(biometric_token)
        except KeyError as error:
            raise UserNotFound() from error

    def remove_biometric_token(self, user_id: int, biometric_token: str):
        """
        This function is used to remove the biometric token of the user.
        """
        try:
            remove_biometric_token_repo(user_id, biometric_token)
        except KeyError as error:
            raise UserNotFound() from error
