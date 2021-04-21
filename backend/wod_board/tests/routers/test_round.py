import daiquiri
import pytest

from wod_board.models import wod


LOG = daiquiri.getLogger(__name__)


@pytest.mark.asyncio
async def test_add_round(db, client):
    wod_type = wod.WodType(name="AMRAP")
    new_wod = wod.Wod(wod_type=wod_type)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    round_json = {
        "position": 1,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": new_wod.id,
        "sub_rounds": [
            {
                "position": 2,
                "wod_id": new_wod.id,
            },
        ],
    }

    response = await client.post("/api/round", json=round_json)

    expected_response = {
        "id": 1,
        "position": 1,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": new_wod.id,
        "parent_id": None,
        "sub_rounds": [
            {
                "id": 2,
                "position": 2,
                "duration_seconds": None,
                "repetition": None,
                "wod_id": new_wod.id,
                "parent_id": 1,
                "sub_rounds": [],
                "movements": [],
            },
        ],
        "movements": [],
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_add_round_with_wrong_wod_id(db, client):
    round_json = {
        "position": 1,
        "wod_id": 0,
        "sub_rounds": [],
        "movements": [],
    }

    response = await client.post("/api/round", json=round_json)

    assert response.status_code == 422
    assert response.json() == {"detail": "The given WOD id is unknown"}


@pytest.mark.asyncio
async def test_add_rounds_with_same_position(db, client):
    wod_type = wod.WodType(name="AMRAP")
    new_wod = wod.Wod(wod_type=wod_type)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    round_json = {
        "position": 1,
        "wod_id": new_wod.id,
        "sub_rounds": [
            {
                "position": 1,
                "wod_id": new_wod.id,
                "sub_rounds": [],
            },
        ],
        "movements": [],
    }

    response = await client.post("/api/round", json=round_json)

    assert response.status_code == 422
    assert response.json() == {"detail": "Rounds have the same position"}
