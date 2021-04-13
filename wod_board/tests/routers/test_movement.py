import daiquiri
import pytest

from wod_board.models import movement


LOG = daiquiri.getLogger(__name__)


@pytest.mark.asyncio
async def test_add(db, client):
    movement_json = {"name": "Devil Press", "unit_id": None, "equipments": []}
    response = await client.post("/api/movement/", json=movement_json)

    expected_response = {
        "id": 1,
        "name": "Devil Press",
        "unit_id": None,
        "unit": None,
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
        "unit": None,
        "equipments": [],
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_add_goal(db, client):
    movement_json = {
        "movement": {
            "name": "Devil Press",
        },
    }
    response = await client.post("/api/movement/goal", json=movement_json)

    expected_response = {
        "id": 1,
        "movement_id": 1,
        "movement": {
            "equipments": [],
            "id": 1,
            "name": "Devil Press",
            "unit": None,
            "unit_id": None,
        },
        "equipments": [],
        "repetition": None,
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_movement_goal_by_id(db, client):
    response = await client.get("/api/movement/goal/1")

    expected_response = {"detail": "This goal doesn't exist yet"}

    assert response.status_code == 404
    assert response.json() == expected_response

    wanted_movement = movement.Movement(name="Devil Press")
    goal = movement.MovementGoal(movement=wanted_movement)
    db.add(goal)
    db.commit()
    db.refresh(goal)

    response = await client.get(f"/api/movement/goal/{goal.id}")

    expected_response = {
        "id": 1,
        "movement_id": 1,
        "movement": {
            "equipments": [],
            "id": 1,
            "name": "Devil Press",
            "unit": None,
            "unit_id": None,
        },
        "equipments": [],
        "repetition": None,
    }

    assert response.status_code == 200
    assert response.json() == expected_response
