# user_tests.py

"""
This is the test module.
"""
from datetime import datetime

import pytest
from service.user import User

# from service.user import get_user_username
from service.user import remove_user_email
from service.user import get_user_email
from service.user import try_login
from service.user import get_user_username
from service.user import make_admin
from service.user import remove_admin_status
from service.user import create_follow
from service.user import get_following_count
from service.user import get_followers_count
from service.user import get_all_followers
from service.user import get_all_following
from service.user import remove_follow
from service.user import get_user_password
from service.user import change_password
from service.user import remove_user_username
from service.user import change_bio
from service.user import change_avatar
from service.user import change_name
from service.user import change_date_of_birth
from service.user import change_last_name
from service.errors import UserNotFound
from service.errors import EmailAlreadyRegistered, UsernameAlreadyRegistered
from service.errors import PasswordDoesntMatch, FollowingRelationAlreadyExists
from service.errors import UserCantFollowItself

EMAIL = "real_email@gmail.com"
USERNAME = "real_username"
PASSWORD = "Real_password123"


def remove_test_user_from_db():
    """
    This function removes the test user from the database.
    """
    try:
        remove_user_email(EMAIL)
    except UserNotFound:
        return


def save_test_user_to_db():
    """
    This function saves the test user to the database.
    """
    user = User(
        email=EMAIL,
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username=USERNAME,
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
    )

    user.save()


def test_user_can_login_after_register():
    """
    This function tests that the user is registered and can login.
    """
    remove_test_user_from_db()

    user = User(
        email=EMAIL,
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username=USERNAME,
        date_of_birth="666 6 6",
        bio="Real_bio",
    )

    user.save()

    assert try_login(EMAIL, PASSWORD) == {"message": "Login successful"}

    remove_user_email(EMAIL)


def test_user_get_username():
    """
    This function tests the user get by username.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    repo_user = get_user_username(USERNAME)

    assert repo_user.username == USERNAME

    remove_user_email(EMAIL)


def test_user_get_username_wrong_nick():
    """
    This function tries to get the user but the nick doesn't exist
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        get_user_username("wrong_nick")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_user_get_email():
    """
    This function tests the user get by email.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    repo_user = get_user_email(EMAIL)

    assert repo_user.email == EMAIL

    remove_user_email(EMAIL)


def test_remove_user():
    """
    This function tests the user remove.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    remove_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        get_user_email(EMAIL)
    assert str(error.value) == "User not found"


def test_user_already_registered_email():
    """
    This function tests the exception of user already registered (email).
    """

    remove_test_user_from_db()

    user = User(
        email="email_repe",
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username="nick_no_repe",
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
    )

    user.save()
    user.username = "username_no_repe1"
    with pytest.raises(EmailAlreadyRegistered) as error:
        user.save()
    assert str(error.value) == "Email already registered"

    remove_user_email("email_repe")


def test_user_already_registered_username():
    """
    This function tests the exception of user already registered (username).
    """

    remove_test_user_from_db()

    user = User(
        email="email_no_repe",
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username="username_repe",
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
    )

    user.save()
    user.email = "email_no_repe1"
    with pytest.raises(UsernameAlreadyRegistered) as error:
        user.save()
    assert str(error.value) == "Username already registered"

    remove_user_email("email_no_repe")


def test_wrong_password():
    """
    This function tests the exception of wrong password.
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(PasswordDoesntMatch) as error:
        try_login(EMAIL, "wrong_password")
    assert str(error.value) == "Password doesn't match"

    remove_user_email(EMAIL)


def test_setters_work():
    """
    This function tests the setters.
    """

    remove_test_user_from_db()

    user = User()

    user.set_email(EMAIL)
    user.set_password(PASSWORD)
    user.set_name("Real_name")
    user.set_surname("Real_surname")
    user.set_username(USERNAME)
    user.set_date_of_birth("666 6 6")
    user.set_bio("Real_bio")
    user.set_avatar("image.png")
    user.set_admin(True)

    assert user.email == EMAIL
    assert user.password == PASSWORD
    assert user.name == "Real_name"
    assert user.surname == "Real_surname"
    assert user.username == USERNAME
    assert user.date_of_birth == "666 6 6"
    assert user.bio == "Real_bio"
    assert user.avatar == "image.png"
    assert user.admin is True


def test_user_login():
    """
    This function tests the user login.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    assert try_login(EMAIL, PASSWORD) == {"message": "Login successful"}

    remove_user_email(EMAIL)


def test_user_login_wrong_password():
    """
    This function tests the exception password doesn't match
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(PasswordDoesntMatch) as error:
        try_login(EMAIL, "wrong_password")
    assert str(error.value) == "Password doesn't match"

    remove_user_email(EMAIL)


def test_user_login_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        try_login("wrong_email", PASSWORD)
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_user_remove_by_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        remove_user_email("wrong_email")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_user_can_be_set_as_admin():
    """
    This function makes and admin, and then
    checks if the user is an admin.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    make_admin(EMAIL)

    assert get_user_email(EMAIL).admin is True

    remove_user_email(EMAIL)


def test_user_can_be_removed_of_its_admin_priviliges():
    """
    This function makes and admin, and then
    checks if the user is an admin.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    make_admin(EMAIL)

    assert get_user_email(EMAIL).admin is True

    remove_admin_status(EMAIL)

    assert get_user_email(EMAIL).admin is False

    remove_user_email(EMAIL)


def test_user_can_follow_another_user():
    """
    This function tests that a user can follow another user.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    user_to_be_followed = User(
        email=EMAIL + "1",
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username=USERNAME + "1",
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
    )

    user_to_be_followed.save()

    user = get_user_email(EMAIL)

    create_follow(user.email, user_to_be_followed.email)

    assert get_following_count(user.email) == 1
    assert get_followers_count(user_to_be_followed.email) == 1

    followers = get_all_followers(user_to_be_followed.email)

    assert followers[0].username == user.username

    following = get_all_following(user.email)

    assert following[0].username == user_to_be_followed.username

    remove_follow(user.email, user_to_be_followed.email)
    remove_user_email(EMAIL)
    remove_user_email(EMAIL + "1")


def test_user_cant_follow_the_same_user_twice():
    """
    This function tests that a user can't follow the same user twice.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    user_to_be_followed = User(
        email=EMAIL + "1",
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username=USERNAME + "1",
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
    )

    user_to_be_followed.save()

    user = get_user_email(EMAIL)

    create_follow(user.email, user_to_be_followed.email)

    assert get_following_count(user.email) == 1
    assert get_followers_count(user_to_be_followed.email) == 1

    with pytest.raises(FollowingRelationAlreadyExists) as error:
        create_follow(user.email, user_to_be_followed.email)
    assert str(error.value) == "Following relation already exists!"

    remove_follow(user.email, user_to_be_followed.email)
    remove_user_email(EMAIL)
    remove_user_email(EMAIL + "1")


def test_user_cant_follow_itself():
    """
    This function tests that a user can't follow itself.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    user = get_user_email(EMAIL)

    with pytest.raises(UserCantFollowItself) as error:
        create_follow(user.email, user.email)
    assert str(error.value) == "User can't follow itself!"

    remove_user_email(EMAIL)


def test_user_cant_follow_user_that_doesnt_exist():
    """
    This function tests that a user can't follow a user that doesn't exist.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    user = get_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        create_follow(user.email, "wrong_email")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_user_cant_be_followed_by_a_user_that_doesnt_exist():
    """
    This function tests that a user can't be followed by a user that doesn't exist.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    user = get_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        create_follow("wrong_email", user.email)
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_get_user_password():
    """
    This function tests the get user password.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    assert get_user_password(EMAIL) == PASSWORD

    remove_user_email(EMAIL)


def test_get_user_password_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        get_user_password("wrong_email")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_update_user_password():
    """
    This function tests the update user password.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_password(EMAIL, "new_password")

    assert get_user_password(EMAIL) == "new_password"

    remove_user_email(EMAIL)


def test_update_user_password_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_password("wrong_email", "new_password")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_remove_user_by_username():
    """
    This function tests the remove user by username.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    remove_user_username(USERNAME)

    with pytest.raises(UserNotFound) as error:
        get_user_email(EMAIL)
    assert str(error.value) == "User not found"


def test_remove_user_by_username_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        remove_user_username("wrong_username")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_make_user_admin_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        make_admin("wrong_email")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_remove_admin_priviliges_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        remove_admin_status("wrong_email")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_get_following_count_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        get_following_count("wrong_username")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_remove_follow_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    user_to_be_followed = User(
        email=EMAIL + "1",
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username=USERNAME + "1",
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
    )

    user_to_be_followed.save()

    user = get_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        remove_follow(user.email, "wrong_username")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)
    remove_user_email(EMAIL + "1")


def test_remove_user_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        remove_user_username("wrong_username")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_get_all_followers_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    user_to_be_followed = User(
        email=EMAIL + "1",
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username=USERNAME + "1",
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
    )

    user_to_be_followed.save()

    user = get_user_email(EMAIL)

    create_follow(user.email, user_to_be_followed.email)

    with pytest.raises(UserNotFound) as error:
        get_all_followers("wrong_username")
    assert str(error.value) == "User not found"

    remove_follow(user.email, user_to_be_followed.email)
    remove_user_email(EMAIL)
    remove_user_email(EMAIL + "1")


def test_get_all_following_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    user_to_be_followed = User(
        email=EMAIL + "1",
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username=USERNAME + "1",
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
    )

    user_to_be_followed.save()

    user = get_user_email(EMAIL)

    create_follow(user.email, user_to_be_followed.email)

    with pytest.raises(UserNotFound) as error:
        get_all_following("wrong_username")
    assert str(error.value) == "User not found"

    remove_follow(user.email, user_to_be_followed.email)
    remove_user_email(EMAIL)
    remove_user_email(EMAIL + "1")


def test_change_user_bio():
    """
    This function tests the change user bio.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_bio(EMAIL, "new_bio")

    assert get_user_email(EMAIL).bio == "new_bio"

    remove_user_email(EMAIL)


def test_change_user_bio_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_bio("wrong_email", "new_bio")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_change_user_avatar():
    """
    This function tests the change user avatar.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_avatar(EMAIL, "new_avatar")

    assert get_user_email(EMAIL).avatar == "new_avatar"

    remove_user_email(EMAIL)


def test_change_user_avatar_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_avatar("wrong_email", "new_avatar")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_change_user_name():
    """
    This function tests the change user name.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_name(EMAIL, "new_name")

    assert get_user_email(EMAIL).name == "new_name"

    remove_user_email(EMAIL)


def test_change_user_name_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_name("wrong_email", "new_name")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_change_user_date_of_birth():
    """
    This function tests the change user date of birth.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_date_of_birth(EMAIL, "999 9 9")

    assert get_user_email(EMAIL).date_of_birth == datetime(999, 9, 9)

    remove_user_email(EMAIL)


def test_change_user_date_of_birth_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_date_of_birth("wrong_email", "999 9 9")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_change_user_last_name():
    """
    This function tests the change user last name.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_last_name(EMAIL, "new_last_name")

    assert get_user_email(EMAIL).surname == "new_last_name"

    remove_user_email(EMAIL)


def test_change_user_last_name_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_last_name("wrong_email", "new_last_name")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_remove_user_username_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        remove_user_username("wrong_username")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)
