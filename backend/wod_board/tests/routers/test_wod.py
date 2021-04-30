import pytest

from wod_board.models import wod


@pytest.mark.asyncio
async def test_create_wod(db, client, db_user):
    wod_type = wod.WodType(name="For Time")
    db.add(wod_type)
    db.commit()
    db.refresh(wod_type)

    wod_json = {
        "title": "Murph",
        "description": "Murph Day!",
        "date": "2021-03-24T14:42:46.580110",
        "author_id": 2,
        "wod_type_id": wod_type.id,
    }
    response = await client.post("/api/wod", json=wod_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This author is unknown"}

    wod_json = {
        "title": "Murph",
        "description": "Murph Day!",
        "date": "2021-03-24T14:42:46.580110",
        "author_id": db_user.id,
        "wod_type_id": 2,
    }
    response = await client.post("/api/wod", json=wod_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This WOD Type doesn't exist"}
    assert db.query(wod.Wod).count() == 0

    wod_json = {
        "title": "Murph",
        "description": "Murph Day!",
        "date": "2021-03-24T14:42:46.580110",
        "author_id": db_user.id,
        "wod_type_id": wod_type.id,
    }
    response = await client.post("/api/wod", json=wod_json)
    expected_response = {
        "id": 3,
        "title": "Murph",
        "description": "Murph Day!",
        "date": "2021-03-24T14:42:46.580110",
        "author_id": db_user.id,
        "wod_type_id": wod_type.id,
        "rounds": [],
        "wod_type": {
            "id": wod_type.id,
            "name": wod_type.name,
        },
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(wod.Wod).count() == 1

    response = await client.post("/api/wod", json=wod_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This title is already used"}
    assert db.query(wod.Wod).count() == 1


@pytest.mark.asyncio
async def test_update_wod(db, client, db_user):
    db_wod = wod.Wod(title="Murph", author_id=db_user.id)
    db.add(db_wod)
    db.add(wod.Wod(title="Cindy", author_id=db_user.id))
    db.commit()
    db.refresh(db_wod)

    assert db.query(wod.Wod).count() == 2

    wod_json = {
        "title": "Karen",
        "author_id": db_user.id,
    }
    response = await client.put(f"/api/wod/{db_wod.id}", json=wod_json)
    assert response.status_code == 200
    assert response.json()["title"] == wod_json["title"]
    assert db.query(wod.Wod).count() == 2

    response = await client.put("/api/wod/3", json=wod_json)
    assert response.status_code == 404
    assert response.json() == {"detail": "This WOD doesn't exist"}
    assert db.query(wod.Wod).count() == 2

    wod_json = {
        "title": "Karen",
        "author_id": db_user.id,
        "wod_type_id": 1,
    }
    response = await client.put(f"/api/wod/{db_wod.id}", json=wod_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This WOD Type doesn't exist"}
    assert db.query(wod.Wod).count() == 2

    wod_json = {
        "title": "Karen",
        "author_id": 2,
    }
    response = await client.put(f"/api/wod/{db_wod.id}", json=wod_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This author is unknown"}
    assert db.query(wod.Wod).count() == 2

    wod_json = {
        "title": "Cindy",
        "author_id": db_user.id,
    }
    response = await client.put(f"/api/wod/{db_wod.id}", json=wod_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This title is already used"}
    assert db.query(wod.Wod).count() == 2


@pytest.mark.asyncio
async def test_get_wod_by_id(db, client, db_user):
    db_wod = wod.Wod(title="Murph", author_id=db_user.id)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    response = await client.get(f"/api/wod/{db_wod.id}")
    assert response.status_code == 200
    assert response.json()["id"] == db_wod.id

    response = await client.get("/api/wod/2")
    assert response.status_code == 422
    assert response.json() == {"detail": "This WOD doesn't exist"}


@pytest.mark.asyncio
async def test_get_wod_types_by_name(db, client):
    response = await client.get("/api/wod/types/AMRAP")
    assert response.status_code == 200
    assert response.json() == []

    db.add(wod.WodType(name="For Time"))
    db.add(wod.WodType(name="For Load"))
    db.commit()

    response = await client.get("/api/wod/types/for")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = await client.get("/api/wod/types/loa")
    assert response.status_code == 200
    assert len(response.json()) == 1
