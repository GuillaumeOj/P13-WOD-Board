from unittest import mock

import pytest

from wod_board.models import user
from wod_board.utils import user_utils


@pytest.mark.asyncio
async def test_register(db, client):
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

    assert response.status_code == 200

    expected_response = user_json.copy()
    del expected_response["password"]
    expected_response["id"] = 1

    assert response.json() == expected_response

    users = db.query(user.User).all()
    assert len(users) == 1

    response = await client.post(
        "/api/user/register",
        headers={"X-Token": "foobar"},
        data=user_json,
    )

    assert response.status_code == 400
    assert response.json() == {"detail": [{"msg": "Email already used"}]}

    users = db.query(user.User).all()
    assert len(users) == 1

    user_json2 = user_json.copy()
    user_json2["email"] = "foo2@bar.com"

    response = await client.post(
        "/api/user/register",
        headers={"X-Token": "foobar"},
        data=user_json2,
    )

    assert response.status_code == 400
    assert response.json() == {"detail": [{"msg": "Username already used"}]}

    users = db.query(user.User).all()
    assert len(users) == 1


@pytest.mark.asyncio
async def test_login(db, client):
    password = "strong-password"
    hashed_password = user_utils.PASSWORD_CTXT.hash(password)
    user_account = user.User(
        email="foo@bar.com",
        username="foo_bar",
        hashed_password=hashed_password,
    )
    db.add(user_account)
    db.commit()
    db.refresh(user_account)

    user_data = {
        "username": user_account.email,
        "password": password,
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
