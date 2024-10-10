from datetime import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import SecretStr
from requests.auth import HTTPBasicAuth

from homework_4.api.users import router
from homework_4.core.users import UserEntity, UserInfo, UserRole, UserService


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    app.state.user_service = UserService(password_validators=[])
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def mock_admin_dep():
    return UserEntity(
        uid=0,
        info=UserInfo(
            username="admin",
            name="Admin User",
            birthdate=datetime(1980, 1, 1),
            role=UserRole.ADMIN,
            password=SecretStr("adminpassword"),
        ),
    )


@pytest.fixture
def mock_author_dep():
    return UserEntity(
        uid=0,
        info=UserInfo(
            username="testuser",
            name="Test User",
            birthdate=datetime(1990, 1, 1),
            role=UserRole.USER,
            password=SecretStr("password123"),
        ),
    )


@pytest.fixture
def admin_auth():
    return HTTPBasicAuth("admin", "adminpassword")


@pytest.fixture
def author_auth():
    return HTTPBasicAuth("testuser", "password123")


def test_register_user(client, mock_admin_dep, admin_auth):
    response = client.post(
        "/user-register",
        json={
            "username": "testuser",
            "name": "Test User",
            "birthdate": "1990-01-01T00:00:00",
            "password": "password123",
        },
        auth=admin_auth,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["name"] == "Test User"
    assert data["birthdate"] == "1990-01-01T00:00:00"
    assert data["role"] == UserRole.USER


def test_register_duplicate_user(client, mock_admin_dep, admin_auth):
    client.app.state.user_service.register(mock_admin_dep.info)
    client.post(
        "/user-register",
        json={
            "username": "testuser",
            "name": "Test User",
            "birthdate": "1990-01-01T00:00:00",
            "password": "password123",
        },
        auth=admin_auth,
    )
    with pytest.raises(ValueError):
        client.post(
            "/user-register",
            json={
                "username": "testuser",
                "name": "Test User",
                "birthdate": "1990-01-01T00:00:00",
                "password": "password123",
            },
            auth=admin_auth,
        )


def test_get_user_by_id(client, mock_author_dep, author_auth):
    client.app.state.user_service.register(mock_author_dep.info)
    response = client.post("/user-get?id=1", auth=author_auth)
    print(123)
    print(client.app.state.user_service._data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_get_user_by_username(client, mock_author_dep, author_auth):
    client.app.state.user_service.register(mock_author_dep.info)
    response = client.post("/user-get?username=testuser", auth=author_auth)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_get_user_both_id_and_username(client, mock_admin_dep, admin_auth):
    client.app.state.user_service.register(mock_admin_dep.info)
    with pytest.raises(ValueError, match="both id and username are provided"):
        client.post("/user-get?id=1&username=testuser", auth=admin_auth)


def test_get_user_neither_id_nor_username(client, mock_admin_dep, admin_auth):
    client.app.state.user_service.register(mock_admin_dep.info)
    with pytest.raises(ValueError, match="neither id nor username are provided"):
        client.post("/user-get", auth=admin_auth)


def test_get_user_not_found(client, mock_admin_dep, admin_auth):
    client.app.state.user_service.register(mock_admin_dep.info)
    response = client.post("/user-get?id=999", auth=admin_auth)
    assert response.status_code == 404


def test_promote_user(client, mock_author_dep, mock_admin_dep, admin_auth):
    client.app.state.user_service.register(mock_author_dep.info)
    client.app.state.user_service.register(mock_admin_dep.info)

    response = client.post("/user-promote?id=2", auth=admin_auth)
    assert response.status_code == 200
    promoted_user = client.app.state.user_service.get_by_id(2)
    assert promoted_user.info.role == UserRole.ADMIN


def test_promote_user_not_found(client, mock_admin_dep, admin_auth):
    client.app.state.user_service.register(mock_admin_dep.info)

    with pytest.raises(ValueError, match="user not found"):
        client.post("/user-promote?id=999", auth=admin_auth)
