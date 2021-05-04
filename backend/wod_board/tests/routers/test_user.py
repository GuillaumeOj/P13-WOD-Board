from unittest import mock

import pytest

from wod_board.models import user
from wod_board.utils import user_utils


@pytest.mark.asyncio
async def test_register(db, client):
    assert db.query(user.User).count() == 0
    user_json = {
        "email": "foo@bar.com",
        "username": "foo_bar",
        "first_name": "foo",
        "last_name": "bar",
        "password": "strong-password",
    }
    response = await client.post(
        "/api/user/register",
        headers={"X-Token": "foobar"},
        data=user_json,
    )
    expected_response = user_json.copy()
    del expected_response["password"]
    expected_response["id"] = 1
    expected_response["is_admin"] = None
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(user.User).count() == 1

    response = await client.post(
        "/api/user/register",
        headers={"X-Token": "foobar"},
        data=user_json,
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Email already used"}
    assert db.query(user.User).count() == 1

    user_json2 = user_json.copy()
    user_json2["email"] = "foo2@bar.com"
    response = await client.post(
        "/api/user/register",
        headers={"X-Token": "foobar"},
        data=user_json2,
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Username already used"}
    assert db.query(user.User).count() == 1


@pytest.mark.asyncio
async def test_login(client, db_user):
    user_data = {
        "username": db_user.email,
        "password": "very-strong-password",
    }
    foo_token = "foo-token"
    with mock.patch("jose.jwt.encode") as mocked_encode:
        mocked_encode.return_value = foo_token
        response = await client.post(
            "/api/user/token",
            data=user_data,
        )
    assert response.status_code == 200
    assert response.json() == {"access_token": foo_token, "token_type": "bearer"}

    user_data = {
        "username": "bar@foo.com",
        "password": "very-strong-password",
    }
    with mock.patch("jose.jwt.encode") as mocked_encode:
        mocked_encode.return_value = foo_token
        response = await client.post(
            "/api/user/token",
            data=user_data,
        )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}

    user_data = {
        "username": db_user.email,
        "password": "dummy-password",
    }
    with mock.patch("jose.jwt.encode") as mocked_encode:
        mocked_encode.return_value = foo_token
        response = await client.post(
            "/api/user/token",
            data=user_data,
        )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


@pytest.mark.asyncio
async def test_get_current_user(client, db_user, token):
    response = await client.get(
        "/api/user/current", headers={"Authorization": f"Bearer {token.access_token}"}
    )
    expected_response = {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "is_admin": db_user.is_admin,
    }
    assert response.status_code == 200
    assert response.json() == expected_response

    response = await client.get(
        "/api/user/current", headers={"Authorization": "Bearer foo-token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}

    token = user_utils.create_access_token(user.User(email="foo@email.com"))
    response = await client.get(
        "/api/user/current", headers={"Authorization": f"Bearer {token.access_token}"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
