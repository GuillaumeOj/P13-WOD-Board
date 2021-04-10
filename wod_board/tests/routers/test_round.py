import pytest

from wod_board.models import wod


@pytest.mark.asyncio
async def test_add_round(db, client):
    wod_type = wod.WodType("foo")
    db.add(wod_type)
    db.commit()
    db.refresh(wod_type)
    new_wod = wod.Wod(wod_type_id=wod_type.id)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    round_json = {
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

    response = await client.post("/api/round", json=round_json)

    expected_response = {
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

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_add_round_with_wrong_wod_id(db, client):
    round_json = {
        "position": 1,
        "duration_seconds": 0,
        "wod_id": 0,
        "children": [],
    }

    response = await client.post("/api/round", json=round_json)

    assert response.status_code == 422
    assert response.json() == {"detail": "The given WOD id is unknown"}


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

    round_json = {
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

    response = await client.post("/api/round", json=round_json)

    assert response.status_code == 422
    assert response.json() == {"detail": "Rounds have the same position"}
