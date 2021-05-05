import pytest

from wod_board.models import goal


@pytest.mark.asyncio
async def test_create_goal(db, client, db_round, db_movement):
    assert db.query(goal.Goal).count() == 0

    goal_json = {
        "movement_id": db_movement.id,
        "round_id": db_round.id,
        "repetition": 10,
        "duration_seconds": 60 * 5,
    }
    response = await client.post("/api/goal", json=goal_json)
    expected_response = goal_json | {
        "id": 1,
        "equipments": [],
        "movement": {
            "equipments": db_movement.equipments.all(),
            "id": db_movement.id,
            "name": db_movement.name,
            "unit": {
                "id": db_movement.unit.id,
                "name": db_movement.unit.name,
                "symbol": db_movement.unit.symbol,
            },
            "unit_id": db_movement.unit.id,
        },
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(goal.Goal).count() == 1

    goal_json = {
        "repetition": 10,
        "round_id": 2,
        "movement_id": db_movement.id,
    }
    response = await client.post("/api/goal", json=goal_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This round doesn't exist"}
    assert db.query(goal.Goal).count() == 1

    goal_json = {"repetition": 10, "round_id": db_round.id, "movement_id": 2}
    response = await client.post("/api/goal", json=goal_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This goal doesn't exist"}
    assert db.query(goal.Goal).count() == 1


@pytest.mark.asyncio
async def test_update_goal(db, client, db_goal):
    assert db.query(goal.Goal).count() == 1

    goal_json = {
        "movement_id": db_goal.movement_id,
        "round_id": db_goal.round_id,
        "repetition": 10,
        "duration_seconds": 60 * 5,
    }
    response = await client.put(f"/api/goal/{db_goal.id}", json=goal_json)
    expected_response = goal_json | {
        "id": 1,
        "equipments": [],
        "movement": {
            "equipments": db_goal.movement.equipments.all(),
            "id": db_goal.movement.id,
            "name": db_goal.movement.name,
            "unit": {
                "id": db_goal.movement.unit.id,
                "name": db_goal.movement.unit.name,
                "symbol": db_goal.movement.unit.symbol,
            },
            "unit_id": db_goal.movement.unit.id,
        },
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(goal.Goal).count() == 1

    response = await client.put("/api/goal/2", json=goal_json)
    assert response.status_code == 404
    assert response.json() == {"detail": "This goal doesn't exist"}
    assert db.query(goal.Goal).count() == 1

    goal_json = {
        "movement_id": 2,
        "round_id": db_goal.round_id,
        "repetition": 10,
        "duration_seconds": 60 * 5,
    }
    response = await client.put(f"/api/goal/{db_goal.id}", json=goal_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This movement doesn't exist"}
    assert db.query(goal.Goal).count() == 1

    goal_json = {
        "movement_id": db_goal.movement_id,
        "round_id": 2,
        "repetition": 10,
        "duration_seconds": 60 * 5,
    }
    response = await client.put(f"/api/goal/{db_goal.id}", json=goal_json)
    assert response.status_code == 422
    assert response.json() == {"detail": "This round doesn't exist"}
    assert db.query(goal.Goal).count() == 1


@pytest.mark.asyncio
async def test_get_goal_by_id(client, db_goal):
    response = await client.get("/api/goal/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "This goal doesn't exist"}

    response = await client.get(f"/api/goal/{db_goal.id}")
    expected_response = {
        "id": 1,
        "round_id": db_goal.round_id,
        "movement_id": db_goal.movement_id,
        "repetition": None,
        "duration_seconds": None,
        "equipments": [],
        "movement": {
            "equipments": db_goal.movement.equipments.all(),
            "id": db_goal.movement.id,
            "name": db_goal.movement.name,
            "unit": {
                "id": db_goal.movement.unit.id,
                "name": db_goal.movement.unit.name,
                "symbol": db_goal.movement.unit.symbol,
            },
            "unit_id": db_goal.movement.unit.id,
        },
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_delete_goal_by_id(db, client, db_goal):
    assert db.query(goal.Goal).count() == 1

    response = await client.get("/api/goal/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "This goal doesn't exist"}
    assert db.query(goal.Goal).count() == 1

    response = await client.delete(f"/api/goal/{db_goal.id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Goal successfully deleted"}
    assert db.query(goal.Goal).count() == 0
