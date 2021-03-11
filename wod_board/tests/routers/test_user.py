from wod_board.models import user as user_models


def test_register(db, client):
    user_json = {
        "email": "foo@bar.com",
        "username": "foo_bar",
        "first_name": "foo",
        "last_name": "bar",
        "password": "strong-password",
    }
    response = client.post(
        "/user/register",
        headers={"X-Token": "foobar"},
        json=user_json,
    )

    assert response.status_code == 200

    expected_response = user_json.copy()
    del expected_response["password"]
    expected_response["id"] = 1

    assert response.json() == expected_response

    users = db.query(user_models.User).all()
    assert len(users) == 1

    response = client.post(
        "/user/register",
        headers={"X-Token": "foobar"},
        json=user_json,
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

    users = db.query(user_models.User).all()
    assert len(users) == 1

    user_json2 = user_json.copy()
    user_json2["email"] = "foo2@bar.com"

    response = client.post(
        "/user/register",
        headers={"X-Token": "foobar"},
        json=user_json2,
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

    users = db.query(user_models.User).all()
    assert len(users) == 1