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
    response = await client.post("/api/wod/add", json=wod_json)

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
async def test_add_rounds(db, client):
    wod_type = wod.WodType("foo")
    db.add(wod_type)
    db.commit()
    db.refresh(wod_type)
    new_wod = wod.Wod(wod_type_id=wod_type.id)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    rounds = [
        {
            "position": 1,
            "duration_seconds": 0,
            "wod_id": new_wod.id,
            "children": [
                {
                    "position": 2,
                    "duration_seconds": 0,
                    "wod_id": new_wod.id,
                    "children": [],
                },
            ],
        }
    ]

    response = await client.post("/api/wod/add/rounds", json=rounds)

    expected_response = [
        {
            "id": 1,
            "position": 1,
            "duration_seconds": 0,
            "wod_id": new_wod.id,
            "parent_id": None,
            "children": [
                {
                    "id": 2,
                    "position": 2,
                    "duration_seconds": 0,
                    "wod_id": new_wod.id,
                    "parent_id": 1,
                    "children": [],
                },
            ],
        }
    ]

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_add_rounds_with_wrong_wod_id(db, client):
    rounds = [
        {
            "position": 1,
            "duration_seconds": 0,
            "wod_id": 0,
            "children": [
                {
                    "position": 2,
                    "duration_seconds": 0,
                    "wod_id": 0,
                    "children": [],
                },
            ],
        }
    ]

    response = await client.post("/api/wod/add/rounds", json=rounds)

    expected_response = {"detail": "The WOD may be created first"}

    assert response.status_code == 422
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_add_rounds_with_same_position(db, client):
    wod_type = wod.WodType("foo")
    db.add(wod_type)
    db.commit()
    db.refresh(wod_type)
    new_wod = wod.Wod(wod_type_id=wod_type.id)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    rounds = [
        {
            "position": 1,
            "duration_seconds": 0,
            "wod_id": new_wod.id,
            "children": [
                {
                    "position": 1,
                    "duration_seconds": 0,
                    "wod_id": new_wod.id,
                    "children": [],
                },
            ],
        }
    ]

    response = await client.post("/api/wod/add/rounds", json=rounds)

    expected_response = {"detail": "Rounds have the same position"}

    assert response.status_code == 422
    assert response.json() == expected_response
