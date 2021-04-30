import pytest

from wod_board.models import wod_round


@pytest.mark.asyncio
async def test_add_round(db, client, db_wod):
    assert db.query(wod_round.Round).count() == 0

    round_json = {
        "position": 1,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": db_wod.id,
        "sub_rounds": [
            {
                "position": 2,
                "wod_id": db_wod.id,
            },
        ],
    }
    response = await client.post("/api/round", json=round_json)
    expected_response = {
        "id": 1,
        "position": 1,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": db_wod.id,
        "parent_id": None,
        "sub_rounds": [
            {
                "id": 2,
                "position": 2,
                "duration_seconds": None,
                "repetition": None,
                "wod_id": db_wod.id,
                "parent_id": 1,
                "sub_rounds": [],
                "movements": [],
            },
        ],
        "movements": [],
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(wod_round.Round).count() == 2

    round_json = {
        "position": 1,
        "wod_id": 0,
        "sub_rounds": [],
        "movements": [],
    }
    response = await client.post("/api/round", json=round_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "The given WOD id is unknown"}
    assert db.query(wod_round.Round).count() == 2

    round_json = {
        "position": 1,
        "wod_id": db_wod.id,
    }
    response = await client.post("/api/round", json=round_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "Rounds have the same position"}
    assert db.query(wod_round.Round).count() == 2


@pytest.mark.asyncio
async def test_update_round(db, client, db_round):
    assert db.query(wod_round.Round).count() == 1

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
    assert db.query(wod_round.Round).count() == 1

    response = await client.put("/api/round/2", json=round_json)
    assert response.status_code == 404
    assert response.json() == {"detail": "This round doesn't exist"}
    assert db.query(wod_round.Round).count() == 1

    round_json = {
        "position": db_round.position,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": 0,
    }
    response = await client.put(f"/api/round/{db_round.id}", json=round_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "The given WOD id is unknown"}
    assert db.query(wod_round.Round).count() == 1

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
    assert db.query(wod_round.Round).count() == 1


@pytest.mark.asyncio
async def test_delete_round_by_id(db, client, db_round):
    assert db.query(wod_round.Round).count() == 1

    response = await client.delete("api/round/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "This round doesn't exist"}
    assert db.query(wod_round.Round).count() == 1

    response = await client.delete(f"api/round/{db_round.id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Round successfully deleted"}
    assert db.query(wod_round.Round).count() == 0


@pytest.mark.asyncio
async def test_get_round_by_id(db, client, db_round):
    assert db.query(wod_round.Round).count() == 1

    response = await client.get("api/round/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "This round doesn't exist"}
    assert db.query(wod_round.Round).count() == 1

    response = await client.get(f"api/round/{db_round.id}")
    expected_response = {
        "id": db_round.id,
        "position": db_round.position,
        "duration_seconds": db_round.duration_seconds,
        "repetition": db_round.repetition,
        "wod_id": db_round.wod_id,
        "parent_id": db_round.parent_id,
        "sub_rounds": [],
        "movements": [],
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(wod_round.Round).count() == 1
