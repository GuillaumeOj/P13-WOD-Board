import pytest

from wod_board.models import movement


@pytest.mark.asyncio
async def test_add(db, client):
    wod_json = {"name": "Devil Press", "unit_id": None, "equipments": []}
    response = await client.post("/api/movement/", json=wod_json)

    expected_response = {
        "id": 1,
        "name": "Devil Press",
        "unit_id": None,
        "equipments": [],
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_movement_by_exact_name(db, client):
    name = "Devil Press"
    response = await client.get(f"/api/movement/{name}")

    expected_response = {"detail": f"{name} doesn't exist yet"}

    assert response.status_code == 404
    assert response.json() == expected_response

    wanted_movement = movement.Movement(name=name)
    db.add(wanted_movement)
    db.commit()

    response = await client.get(f"/api/movement/{name}")

    expected_response = {
        "id": 1,
        "name": "Devil Press",
        "unit_id": None,
        "equipments": [],
    }

    assert response.status_code == 200
    assert response.json() == expected_response
