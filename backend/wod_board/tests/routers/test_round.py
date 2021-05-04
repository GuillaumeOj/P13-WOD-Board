import daiquiri
import pytest

from wod_board.models import wod_round


LOG = daiquiri.getLogger(__name__)


@pytest.mark.asyncio
async def test_create_round(db, client, db_wod, token, admin):
    assert db.query(wod_round.Round).count() == 0

    round_json = {
        "position": 1,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": db_wod.id,
    }
    response = await client.post(
        "/api/round",
        json=round_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    expected_response = {
        "id": 1,
        "position": 1,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": db_wod.id,
        "parent_id": None,
        "sub_rounds": [],
        "movements": [],
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(wod_round.Round).count() == 1

    round_json = {
        "position": 1,
        "wod_id": 0,
        "sub_rounds": [],
        "movements": [],
    }
    response = await client.post(
        "/api/round",
        json=round_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "The given WOD id is unknown"}
    assert db.query(wod_round.Round).count() == 1

    round_json = {
        "position": 1,
        "wod_id": db_wod.id,
    }
    response = await client.post(
        "/api/round",
        json=round_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Rounds have the same position"}
    assert db.query(wod_round.Round).count() == 1

    response = await client.post(
        "/api/round",
        json=round_json,
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert db.query(wod_round.Round).count() == 1

    db_wod.author_id = admin.id
    db.commit()

    response = await client.post(
        "/api/round",
        json=round_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Author don't match with authenticated user"}
    assert db.query(wod_round.Round).count() == 1


@pytest.mark.asyncio
async def test_update_round(db, client, db_round, db_wod, admin, token):
    assert db.query(wod_round.Round).count() == 1

    round_json = {
        "position": db_round.position,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": db_round.wod_id,
    }
    response = await client.put(
        f"/api/round/{db_round.id}",
        json=round_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
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

    response = await client.put(
        "/api/round/2",
        json=round_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This round doesn't exist"}
    assert db.query(wod_round.Round).count() == 1

    response = await client.put(
        f"/api/round/{db_round.id}",
        json=round_json,
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert db.query(wod_round.Round).count() == 1

    round_json = {
        "position": db_round.position,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": 0,
    }
    response = await client.put(
        f"/api/round/{db_round.id}",
        json=round_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "The given WOD id is unknown"}
    assert db.query(wod_round.Round).count() == 1

    db.add(wod_round.Round(position=2, wod_id=db_round.wod_id))
    db.commit()
    assert db.query(wod_round.Round).count() == 2

    round_json = {
        "position": 2,
        "duration_seconds": 60,
        "repetition": 5,
        "wod_id": db_round.wod_id,
        "sub_rounds": [],
    }
    response = await client.put(
        f"/api/round/{db_round.id}",
        json=round_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Rounds have the same position"}
    assert db.query(wod_round.Round).count() == 2

    db_wod.author_id = admin.id
    db.commit()

    response = await client.put(
        f"/api/round/{db_round.id}",
        json=round_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Author don't match with authenticated user"}
    assert db.query(wod_round.Round).count() == 2


@pytest.mark.asyncio
async def test_delete_round_by_id(db, client, db_round, db_wod, db_user, admin, token):
    assert db.query(wod_round.Round).count() == 1

    response = await client.delete(
        "api/round/2", headers={"Authorization": f"Bearer {token.access_token}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "This round doesn't exist"}
    assert db.query(wod_round.Round).count() == 1

    response = await client.delete(
        f"api/round/{db_round.id}",
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert db.query(wod_round.Round).count() == 1

    db_wod.author_id = admin.id
    db.commit()

    response = await client.delete(
        f"api/round/{db_round.id}",
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Author don't match with authenticated user"}
    assert db.query(wod_round.Round).count() == 1

    db_wod.author_id = db_user.id
    db.commit()

    response = await client.delete(
        f"api/round/{db_round.id}",
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
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
