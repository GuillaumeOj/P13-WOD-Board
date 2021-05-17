import pytest

from wod_board.models import goal
from wod_board.schemas import goal_schemas


@pytest.mark.asyncio
async def test_create_goal(db, client, db_round, db_movement, token, token_admin):
    assert db.query(goal.Goal).count() == 0

    goal_json = {
        "movementId": db_movement.id,
        "roundId": db_round.id,
        "repetition": 10,
        "durationSeconds": 60 * 5,
    }
    response = await client.post(
        "/api/goal",
        json=goal_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
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
            "unitId": db_movement.unit.id,
        },
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(goal.Goal).count() == 1

    response = await client.post("/api/goal", json=goal_json)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert db.query(goal.Goal).count() == 1

    response = await client.post(
        "/api/goal",
        json=goal_json,
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Author don't match with authenticated user"}
    assert db.query(goal.Goal).count() == 1

    goal_json = {
        "movementId": db_movement.id,
        "roundId": 2,
        "repetition": 10,
    }
    response = await client.post(
        "/api/goal",
        json=goal_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This round doesn't exist"}
    assert db.query(goal.Goal).count() == 1

    goal_json = {"repetition": 10, "round_id": db_round.id, "movement_id": 2}
    response = await client.post(
        "/api/goal",
        json=goal_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This movement doesn't exist"}
    assert db.query(goal.Goal).count() == 1


@pytest.mark.asyncio
async def test_update_goal(db, client, db_goal, token, token_admin):
    assert db.query(goal.Goal).count() == 1

    goal_json = {
        "movementId": db_goal.movement_id,
        "roundId": db_goal.round_id,
        "repetition": 10,
        "durationSeconds": 60 * 5,
    }
    response = await client.put(
        f"/api/goal/{db_goal.id}",
        json=goal_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
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
            "unitId": db_goal.movement.unit.id,
        },
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(goal.Goal).count() == 1

    response = await client.put(f"/api/goal/{db_goal.id}", json=goal_json)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = await client.put(
        f"/api/goal/{db_goal.id}",
        json=goal_json,
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Author don't match with authenticated user"}

    response = await client.put(
        "/api/goal/2",
        json=goal_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This goal doesn't exist"}

    goal_json = {
        "movementId": 2,
        "roundId": db_goal.round_id,
        "repetition": 10,
        "durationSeconds": 60 * 5,
    }
    response = await client.put(
        f"/api/goal/{db_goal.id}",
        json=goal_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This movement doesn't exist"}

    goal_json = {
        "movementId": db_goal.movement_id,
        "roundId": 2,
        "repetition": 10,
        "durationSeconds": 60 * 5,
    }
    response = await client.put(
        f"/api/goal/{db_goal.id}",
        json=goal_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This round doesn't exist"}


@pytest.mark.asyncio
async def test_delete_goal_by_id(db, client, db_goal, token, token_admin):
    assert db.query(goal.Goal).count() == 1

    response = await client.delete(
        "/api/goal/2", headers={"Authorization": f"Bearer {token.access_token}"}
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This goal doesn't exist"}
    assert db.query(goal.Goal).count() == 1

    response = await client.delete(f"/api/goal/{db_goal.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert db.query(goal.Goal).count() == 1

    response = await client.delete(
        f"/api/goal/{db_goal.id}",
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Author don't match with authenticated user"}
    assert db.query(goal.Goal).count() == 1

    response = await client.delete(
        f"/api/goal/{db_goal.id}",
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Goal successfully deleted"}
    assert db.query(goal.Goal).count() == 0


@pytest.mark.asyncio
async def test_get_goals_by_round_id(db, client, db_goal):
    assert db.query(goal.Goal).count() == 1

    response = await client.get(f"/api/goal/goals/{db_goal.round_id}")
    assert response.status_code == 200
    assert response.json() == [goal_schemas.Goal.from_orm(db_goal).dict(by_alias=True)]

    response = await client.get(f"/api/goal/goals/{db_goal.round_id + 1}")
    assert response.status_code == 200
    assert response.json() == []
