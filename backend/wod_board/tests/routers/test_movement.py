import daiquiri
import pytest

from wod_board.models import movement
from wod_board.models import wod
from wod_board.models import wod_round


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
async def test_add_movement_goal(db, client):
    db_movement = movement.Movement(name="Devil Press")
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)

    db_wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(wod_type=db_wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    db_round = wod_round.Round(position=1, wod_id=db_wod.id)
    db.add(db_round)
    db.commit()
    db.refresh(db_round)

    movement_json = {
        "repetition": 10,
        "round_id": db_round.id,
        "movement": {
            "name": "Devil Press",
        },
    }
    response = await client.post("/api/movement/goal", json=movement_json)

    expected_response = {
        "id": 1,
        "repetition": 10,
        "round_id": db_round.id,
        "movement_id": db_movement.id,
        "movement": {
            "equipments": db_movement.equipments.all(),
            "id": db_movement.id,
            "name": db_movement.name,
            "unit": db_movement.unit,
            "unit_id": db_movement.unit_id,
        },
        "equipments": [],
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_movement_goal_by_id(db, client):
    response = await client.get("/api/movement/goal/1")

    expected_response = {"detail": "This goal doesn't exist yet"}

    assert response.status_code == 404
    assert response.json() == expected_response

    db_wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(wod_type=db_wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    db_round = wod_round.Round(position=1, wod_id=db_wod.id)
    db.add(db_round)
    db.commit()
    db.refresh(db_round)

    wanted_movement = movement.Movement(name="Devil Press")
    goal = movement.MovementGoal(round_id=db_round.id, movement=wanted_movement)
    db.add(goal)
    db.commit()
    db.refresh(goal)

    response = await client.get(f"/api/movement/goal/{goal.id}")

    expected_response = {
        "id": goal.id,
        "round_id": db_round.id,
        "repetition": goal.repetition,
        "movement_id": goal.movement_id,
        "movement": {
            "equipments": goal.movement.equipments.all(),
            "id": goal.movement.id,
            "name": goal.movement.name,
            "unit": goal.movement.unit,
            "unit_id": goal.movement.unit_id,
        },
        "equipments": goal.equipments.all(),
    }

    assert response.status_code == 200
    assert response.json() == expected_response
