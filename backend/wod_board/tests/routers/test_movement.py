import daiquiri
import pytest

from wod_board.models import movement
from wod_board.models import wod
from wod_board.models import wod_round


LOG = daiquiri.getLogger(__name__)


@pytest.mark.asyncio
async def test_add_movement(db, client):
    movement_json = {"name": "Devil Press"}
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
        "movement_id": db_movement.id,
        "round_id": db_round.id,
        "repetition": 10,
        "duration_seconds": 60 * 5,
    }
    response = await client.post("/api/movement/goal", json=movement_json)

    expected_response = movement_json | {
        "id": 1,
        "equipments": [],
        "movement": {
            "equipments": [],
            "id": 1,
            "name": "Devil Press",
            "unit": None,
            "unit_id": None,
        },
    }

    assert response.status_code == 200
    assert response.json() == expected_response

    movement_json = {
        "repetition": 10,
        "round_id": 2,
        "movement_id": db_movement.id,
    }

    response = await client.post("/api/movement/goal", json=movement_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This round doesn't exist"}

    movement_json = {
        "repetition": 10,
        "round_id": db_round.id,
        "movement_id": 2,
    }

    response = await client.post("/api/movement/goal", json=movement_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This goal doesn't exist"}


@pytest.mark.asyncio
async def test_update_movement_goal(db, client):
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

    db_movement_goal = movement.MovementGoal(
        repetition=5, round_id=db_round.id, movement_id=db_movement.id
    )

    db.add(db_movement_goal)
    db.commit()
    db.refresh(db_movement_goal)

    movement_goal_json = {
        "movement_id": db_movement_goal.movement_id,
        "round_id": db_movement_goal.round_id,
        "repetition": 10,
        "duration_seconds": 60 * 5,
    }

    response = await client.put(
        f"/api/movement/goal/{db_movement_goal.id}", json=movement_goal_json
    )

    expected_response = movement_goal_json | {
        "id": 1,
        "equipments": [],
        "movement": {
            "equipments": [],
            "id": 1,
            "name": "Devil Press",
            "unit": None,
            "unit_id": None,
        },
    }

    assert response.status_code == 200
    assert response.json() == expected_response

    response = await client.put("/api/movement/goal/2", json=movement_goal_json)
    assert response.status_code == 404
    assert response.json() == {"detail": "This goal doesn't exist"}

    movement_goal_json = {
        "movement_id": 2,
        "round_id": db_movement_goal.round_id,
        "repetition": 10,
        "duration_seconds": 60 * 5,
    }

    response = await client.put(
        f"/api/movement/goal/{db_movement_goal.id}", json=movement_goal_json
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This movement doesn't exist"}

    movement_goal_json = {
        "movement_id": db_movement_goal.movement_id,
        "round_id": 2,
        "repetition": 10,
        "duration_seconds": 60 * 5,
    }

    response = await client.put(
        f"/api/movement/goal/{db_movement_goal.id}", json=movement_goal_json
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This round doesn't exist"}


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

    devil_press = movement.Movement(name="Devil Press")
    goal = movement.MovementGoal(round_id=db_round.id, movement=devil_press)
    db.add(goal)
    db.commit()
    db.refresh(goal)

    response = await client.get(f"/api/movement/goal/{goal.id}")

    expected_response = {
        "id": 1,
        "round_id": db_round.id,
        "movement_id": goal.movement_id,
        "repetition": None,
        "duration_seconds": None,
        "equipments": [],
        "movement": {
            "equipments": [],
            "id": 1,
            "name": "Devil Press",
            "unit": None,
            "unit_id": None,
        },
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_delete_movement_goal_by_id(db, client):
    db_wod_type = wod.WodType(name="AMRAP")
    db_wod = wod.Wod(wod_type=db_wod_type)
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)

    db_round = wod_round.Round(position=1, wod_id=db_wod.id)
    db.add(db_round)
    db.commit()
    db.refresh(db_round)

    devil_press = movement.Movement(name="Devil Press")
    goal = movement.MovementGoal(round_id=db_round.id, movement=devil_press)
    db.add(goal)
    db.commit()
    db.refresh(goal)

    assert db.query(movement.MovementGoal).count() == 1

    response = await client.get("/api/movement/goal/2")

    assert response.status_code == 404
    assert response.json() == {"detail": "This goal doesn't exist"}

    assert db.query(movement.MovementGoal).count() == 1

    response = await client.delete(f"/api/movement/goal/{goal.id}")

    assert response.status_code == 200
    assert response.json() == {"detail": "Goal successfully deleted"}

    assert db.query(movement.MovementGoal).count() == 0
