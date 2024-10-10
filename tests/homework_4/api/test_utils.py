import json
from datetime import datetime
from http import HTTPStatus

import pytest
from fastapi import HTTPException, Request
from fastapi.security import HTTPBasicCredentials
from pydantic import SecretStr
from starlette.testclient import TestClient

from homework_4.api.main import app
from homework_4.api.utils import initialize, requires_admin, requires_author, user_service, value_error_handler
from homework_4.core.users import UserInfo, UserRole, UserService


@pytest.fixture
def client():
    return TestClient(app)


def test_initialize_service(client):
    response = client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_service_dependency():
    async with initialize(app):
        request = Request(scope={"type": "http", "app": app})
        service = user_service(request)
        assert isinstance(service, UserService)


@pytest.fixture
def mock_user_service():
    service = UserService(password_validators=[])
    service.register(
        UserInfo(
            username="testuser",
            name="Test User",
            birthdate=datetime(1990, 1, 1),
            role=UserRole.USER,
            password=SecretStr("password123"),
        )
    )
    return service


def test_requires_author_valid_credentials(mock_user_service):
    credentials = HTTPBasicCredentials(username="testuser", password="password123")
    user_entity = requires_author(credentials, mock_user_service)
    assert user_entity.info.username == "testuser"


def test_requires_author_invalid_credentials(mock_user_service):
    credentials = HTTPBasicCredentials(username="testuser", password="wrongpassword")
    with pytest.raises(HTTPException) as exc_info:
        requires_author(credentials, mock_user_service)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


def test_requires_author_user_not_found(mock_user_service):
    credentials = HTTPBasicCredentials(username="unknown", password="password123")
    with pytest.raises(HTTPException) as exc_info:
        requires_author(credentials, mock_user_service)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


def test_requires_admin_valid(mock_user_service):
    admin_user_info = UserInfo(
        username="adminuser",
        name="Admin User",
        birthdate=datetime(1980, 1, 1),
        role=UserRole.ADMIN,
        password=SecretStr("adminpassword"),
    )
    admin_user_entity = mock_user_service.register(admin_user_info)
    user_entity = requires_admin(admin_user_entity)
    assert user_entity.info.role == UserRole.ADMIN


def test_requires_admin_non_admin(mock_user_service):
    user_entity = mock_user_service.get_by_username("testuser")
    with pytest.raises(HTTPException) as exc_info:
        requires_admin(user_entity)

    assert exc_info.value.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
async def test_value_error_handler():
    request = Request(scope={"type": "http"})
    response = await value_error_handler(request, ValueError("Invalid input"))
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert json.loads(response.body) == {"detail": "Invalid input"}
