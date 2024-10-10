from datetime import datetime

import pytest
from pydantic import SecretStr

from homework_4.core.users import UserInfo, UserRole, UserService, password_is_longer_than_8


@pytest.fixture
def user_service():
    return UserService(password_validators=[password_is_longer_than_8])


@pytest.fixture
def valid_user_info():
    return UserInfo(
        username="testuser",
        name="Test User",
        birthdate=datetime(1990, 1, 1),
        role=UserRole.USER,
        password=SecretStr("strongpassword123"),
    )


@pytest.mark.parametrize(
    "password, is_valid",
    [
        ("short", False),
        ("longenough", True),
    ],
    ids=["short_password", "valid_password"],
)
def test_password_is_longer_than_8(password, is_valid):
    assert password_is_longer_than_8(password) == is_valid


def test_register_user_success(user_service, valid_user_info):
    user_entity = user_service.register(valid_user_info)
    assert user_entity.uid == 1
    assert user_entity.info.username == "testuser"
    assert user_entity.info.password == valid_user_info.password
    assert user_service.get_by_username("testuser") == user_entity


def test_register_user_duplicate_username(user_service, valid_user_info):
    user_service.register(valid_user_info)

    with pytest.raises(ValueError, match="username is already taken"):
        user_service.register(valid_user_info)


def test_register_user_invalid_password(user_service):
    invalid_user_info = UserInfo(
        username="invaliduser",
        name="Invalid User",
        birthdate=datetime(1990, 1, 1),
        role=UserRole.USER,
        password=SecretStr("short"),
    )

    with pytest.raises(ValueError, match="invalid password"):
        user_service.register(invalid_user_info)


@pytest.mark.parametrize(
    "username, expected",
    [
        ("testuser", True),
        ("nonexistent", False),
    ],
    ids=["existing_user", "non_existing_user"],
)
def test_get_by_username(user_service, valid_user_info, username, expected):
    user_service.register(valid_user_info)

    if expected:
        user_entity = user_service.get_by_username(username)
        assert user_entity.info.username == valid_user_info.username
    else:
        assert user_service.get_by_username(username) is None


def test_get_by_id(user_service, valid_user_info):
    user_entity = user_service.register(valid_user_info)
    assert user_service.get_by_id(user_entity.uid) == user_entity
    assert user_service.get_by_id(999) is None


def test_grant_admin_success(user_service, valid_user_info):
    user_entity = user_service.register(valid_user_info)
    user_service.grant_admin(user_entity.uid)

    assert user_service.get_by_id(user_entity.uid).info.role == UserRole.ADMIN


def test_grant_admin_user_not_found(user_service):
    with pytest.raises(ValueError, match="user not found"):
        user_service.grant_admin(999)


@pytest.mark.parametrize(
    "username, info",
    [
        (
            "admin",
            {
                "username": "admin",
                "name": "Admin User",
                "birthdate": datetime(1970, 1, 1),
                "role": UserRole.ADMIN,
                "password": SecretStr("adminpassword123"),
            },
        ),
        (
            "regular_user",
            {
                "username": "regular_user",
                "name": "Regular User",
                "birthdate": datetime(1990, 1, 1),
                "role": UserRole.USER,
                "password": SecretStr("userpassword123"),
            },
        ),
    ],
    ids=["admin_user", "regular_user"],
)
def test_user_role(user_service, username, info):
    user_info = UserInfo(**info)
    user_entity = user_service.register(user_info)

    assert user_entity.info.role == user_info.role
