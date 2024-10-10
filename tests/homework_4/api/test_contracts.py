from datetime import datetime

import pytest
from pydantic import SecretStr, ValidationError

from homework_4.api.contracts import RegisterUserRequest, UserAuthRequest, UserResponse
from homework_4.core.users import UserEntity, UserInfo, UserRole


def test_register_user_request():
    user_request = RegisterUserRequest(
        username="testuser",
        name="Test User",
        birthdate=datetime(1990, 1, 1),
        password=SecretStr("strongpassword123"),
    )

    assert user_request.username == "testuser"
    assert user_request.name == "Test User"
    assert user_request.birthdate == datetime(1990, 1, 1)
    assert user_request.password.get_secret_value() == "strongpassword123"


def test_register_user_request_invalid_data():
    with pytest.raises(ValidationError):
        RegisterUserRequest(
            username="testuser",
            name="Test User",
            birthdate="invalid date",
            password=SecretStr("strongpassword123"),
        )


def test_user_response_from_user_entity():
    user_info = UserInfo(
        username="testuser",
        name="Test User",
        birthdate=datetime(1990, 1, 1),
        role=UserRole.USER,
        password=SecretStr("strongpassword123"),
    )

    user_entity = UserEntity(uid=1, info=user_info)
    user_response = UserResponse.from_user_entity(user_entity)

    assert user_response.uid == 1
    assert user_response.username == "testuser"
    assert user_response.name == "Test User"
    assert user_response.birthdate == datetime(1990, 1, 1)
    assert user_response.role == UserRole.USER


def test_user_auth_request():
    auth_request = UserAuthRequest(username="testuser", password=SecretStr("strongpassword123"))

    assert auth_request.username == "testuser"
    assert auth_request.password.get_secret_value() == "strongpassword123"


def test_user_auth_request_invalid_data():
    with pytest.raises(ValidationError):
        UserAuthRequest(
            username=12345,
            password=SecretStr("strongpassword123"),
        )
