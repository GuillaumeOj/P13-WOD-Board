import datetime
import json

import pytest

from wod_board.models import wod
from wod_board.schemas import wod_schemas


@pytest.mark.asyncio
async def test_create_wod(db, client, db_user, token):
    wod_json = {
        "title": "Murph",
        "description": "Murph Day!",
        "date": "2021-03-24T14:42:46.580110",
        "authorId": db_user.id,
    }
    response = await client.post(
        "/api/wod",
        json=wod_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    expected_response = wod_json | {
        "id": 1,
        "isComplete": False,
        "wodTypeId": None,
        "rounds": [],
        "wodType": None,
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(wod.Wod).count() == 1

    response = await client.post(
        "/api/wod",
        json=wod_json,
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert db.query(wod.Wod).count() == 1

    wod_json = {
        "title": "Murph",
        "description": "Murph Day!",
        "date": "2021-03-24T14:42:46.580110",
        "authorId": 2,
    }
    response = await client.post(
        "/api/wod",
        json=wod_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Author don't match with authenticated user"}
    assert db.query(wod.Wod).count() == 1

    wod_json = {
        "title": "Murph",
        "description": "Murph Day!",
        "date": "2021-03-24T14:42:46.580110",
        "authorId": db_user.id,
    }
    response = await client.post(
        "/api/wod",
        json=wod_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Title already used"}
    assert db.query(wod.Wod).count() == 1

    wod_json = {
        "title": "Cindy",
        "date": "2021-03-24T14:42:46.580110",
        "authorId": db_user.id,
        "wodTypeId": 2,
    }
    response = await client.post(
        "/api/wod",
        json=wod_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This type doesn't exist"}
    assert db.query(wod.Wod).count() == 1


@pytest.mark.asyncio
async def test_update_wod(db, client, db_user, db_wod, token):
    db.add(
        wod.Wod(
            title="Cindy",
            is_complete=True,
            author_id=db_user.id,
            date=datetime.datetime.utcnow(),
        )
    )
    db.commit()

    assert db.query(wod.Wod).count() == 2

    wod_json = {
        "title": "Karen",
        "authorId": db_user.id,
    }
    response = await client.put(
        f"/api/wod/{db_wod.id}",
        json=wod_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == wod_json["title"]
    assert db.query(wod.Wod).count() == 2

    response = await client.put(
        "/api/wod/3",
        json=wod_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This WOD doesn't exist"}
    assert db.query(wod.Wod).count() == 2

    wod_json = {
        "title": "Karen",
        "authorId": db_user.id,
        "wodTypeId": 1,
    }
    response = await client.put(
        f"/api/wod/{db_wod.id}",
        json=wod_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This type doesn't exist"}
    assert db.query(wod.Wod).count() == 2

    wod_json = {
        "title": "Karen",
        "authorId": 2,
    }
    response = await client.put(
        f"/api/wod/{db_wod.id}",
        json=wod_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Author don't match with authenticated user"}
    assert db.query(wod.Wod).count() == 2

    response = await client.put(f"/api/wod/{db_wod.id}", json=wod_json)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert db.query(wod.Wod).count() == 2

    wod_json = {
        "title": "Cindy",
        "authorId": db_user.id,
    }
    response = await client.put(
        f"/api/wod/{db_wod.id}",
        json=wod_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Title already used"}
    assert db.query(wod.Wod).count() == 2


@pytest.mark.asyncio
async def test_get_wod_by_id(db, client, db_wod):
    assert db.query(wod.Wod).count() == 1

    response = await client.get(f"/api/wod/{db_wod.id}")
    assert response.status_code == 200
    assert response.json()["id"] == db_wod.id
    assert db.query(wod.Wod).count() == 1

    response = await client.get("/api/wod/2")
    assert response.status_code == 422
    assert response.json() == {"detail": "This WOD doesn't exist"}
    assert db.query(wod.Wod).count() == 1


@pytest.mark.asyncio
async def test_get_wod_incomplete(db, client, db_wod, token, token_admin):
    assert db.query(wod.Wod).count() == 1

    response = await client.get(
        "/api/wod/incomplete/",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200
    assert response.json() == json.loads(
        wod_schemas.Wod.from_orm(db_wod).json(by_alias=True)
    )
    assert db.query(wod.Wod).count() == 1

    response = await client.get(
        "/api/wod/incomplete/",
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert db.query(wod.Wod).count() == 1

    response = await client.get(
        "/api/wod/incomplete/",
        headers={
            "Authorization": f"{token_admin.token_type} {token_admin.access_token}"
        },
    )
    assert response.status_code == 200
    assert response.json() is None
    assert db.query(wod.Wod).count() == 1
    assert db.query(wod.Wod).count() == 1


@pytest.mark.asyncio
async def test_get_wods_by_user(db, client, token, db_wod):
    assert db.query(wod.Wod).count() == 1

    response = await client.get(
        "/api/wod/wods/",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200
    assert response.json() == []

    db_wod.is_complete = True
    db.commit()

    response = await client.get(
        "/api/wod/wods/",
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 200
    assert response.json() == [
        json.loads(wod_schemas.Wod.from_orm(db_wod).json(by_alias=True))
    ]
    assert db.query(wod.Wod).count() == 1
