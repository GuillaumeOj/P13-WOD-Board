import pytest

from wod_board.models import wod


@pytest.mark.asyncio
async def test_add_wod(db, client):
    wod_json = {
        "description": "string",
        "note": "string",
        "date": "2021-03-24T14:42:46.580110",
        "wod_type": {
            "name": "string",
        },
    }
    response = await client.post("/api/wod", json=wod_json)

    expected_response = {
        "id": 1,
        "description": "string",
        "note": "string",
        "date": "2021-03-24T14:42:46.580110",
        "rounds": [],
        "wod_type_id": 1,
        "wod_type": {
            "id": 1,
            "name": "string",
        },
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_update_wod(db, client):
    db_wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(note="Bad Note", wod_type=db_wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    wod_json = {
        "description": db_wod.description,
        "note": "Updated Note",
        "date": db_wod.date.isoformat(),
        "wod_type_id": db_wod.wod_type.id,
        "wod_type": {
            "name": db_wod.wod_type.name,
        },
    }
    response = await client.put(f"/api/wod/{db_wod.id}", json=wod_json)

    assert response.status_code == 200
    assert response.json()["note"] == wod_json["note"]

    response = await client.put("/api/wod/2", json=wod_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This WOD doesn't exist"}


@pytest.mark.asyncio
async def test_get_wod_by_id(db, client):
    db_wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(note="Bad Note", wod_type=db_wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    response = await client.get(f"/api/wod/{db_wod.id}")

    assert response.status_code == 200
    assert response.json()["id"] == db_wod.id

    response = await client.get("/api/wod/2")
    assert response.status_code == 422
    assert response.json() == {"detail": "This WOD doesn't exist"}


async def test_get_wod_type_all(db, client):
    response = await client.get("/api/wod/types")

    assert response.status_code == 200
    assert response.json() == []

    db.add(wod.WodType(name="AMRAP"))
    db.commit()

    response = await client.get("/api/wod/types")

    expected_response = [
        {
            "id": 1,
            "name": "AMRAP",
        },
    ]

    assert response.status_code == 200
    assert response.json() == expected_response
