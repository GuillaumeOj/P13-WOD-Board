import daiquiri
import pytest

from wod_board.models import wod
from wod_board.models import wod_round


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
async def test_update_round(db, client):
    db_wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(wod_type=db_wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    db_round = wod_round.Round(position=1, wod_id=db_wod.id)
    db.add(db_round)
    db.commit()
    db.refresh(db_round)

    round_json = {
        "position": db_round.position,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": db_round.wod_id,
    }

    response = await client.put(f"/api/round/{db_round.id}", json=round_json)

    expected_response = {
        "id": db_round.id,
        "position": round_json["position"],
        "duration_seconds": round_json["duration_seconds"],
        "repetition": round_json["repetition"],
        "wod_id": round_json["wod_id"],
        "parent_id": None,
        "sub_rounds": [],
        "movements": [],
    }

    assert response.status_code == 200
    assert response.json() == expected_response

    response = await client.put("/api/round/2", json=round_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This round doesn't exist"}

    round_json = {
        "position": db_round.position,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": 0,
    }

    response = await client.put(f"/api/round/{db_round.id}", json=round_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "The given WOD id is unknown"}

    round_json = {
        "position": db_round.position,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": db_round.wod_id,
        "sub_rounds": [
            {
                "position": db_round.position,
                "duration_seconds": 60,
                "repetition": 5,
                "parent_id": db_round.id,
                "wod_id": db_round.wod_id,
            }
        ],
    }

    response = await client.put(f"/api/round/{db_round.id}", json=round_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "Rounds have the same position"}


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


@pytest.mark.asyncio
async def test_delete_round_by_id(db, client):
    wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(wod_type=wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    db_round = wod_round.Round(wod_id=db_wod.id, position=1)
    db.add(db_round)
    db.commit()
    db.refresh(db_round)

    assert db.query(wod_round.Round).count() == 1

    response = await client.delete("api/round/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "This round doesn't exist"}

    assert db.query(wod_round.Round).count() == 1

    response = await client.delete(f"api/round/{db_round.id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Round successfully deleted"}

    assert db.query(wod_round.Round).count() == 0
