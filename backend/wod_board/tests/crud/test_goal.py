import pytest

from wod_board import exceptions
from wod_board.crud import goal_crud
from wod_board.models import goal
from wod_board.schemas import goal_schemas


def test_create_goal(db, db_round, db_movement):
    assert db.query(goal.Goal).count() == 0

    new_goal = goal_schemas.GoalCreate(
        movement_id=db_movement.id,
        round_id=db_round.id,
        repetition=5,
    )
    assert goal_crud.create_goal(db, new_goal)
    assert db.query(goal.Goal).count() == 1

    new_goal = goal_schemas.GoalCreate(
        movement_id=2,
        round_id=db_round.id,
        repetition=5,
    )
    with pytest.raises(exceptions.UnknownMovement):
        goal_crud.create_goal(db, new_goal)

    new_goal = goal_schemas.GoalCreate(
        movement_id=db_movement.id,
        round_id=2,
        repetition=5,
    )
    with pytest.raises(exceptions.UnknownRound):
        goal_crud.create_goal(db, new_goal)


def test_update_goal(db, db_goal):
    assert db.query(goal.Goal).count() == 1

    goal_schema = goal_schemas.GoalCreate.from_orm(db_goal)
    goal_schema.repetition = 5
    assert db_goal.repetition != goal_schema.repetition

    updated_goal = goal_crud.update_goal(db, goal_schema, db_goal.id)
    assert goal_schema.repetition == updated_goal.repetition
    assert db.query(goal.Goal).count() == 1

    with pytest.raises(exceptions.UnknownGoal):
        goal_crud.update_goal(db, goal_schema, 2)
    assert db.query(goal.Goal).count() == 1

    goal_schema.movement_id = 2
    with pytest.raises(exceptions.UnknownMovement):
        goal_crud.update_goal(db, goal_schema, db_goal.id)
    assert db.query(goal.Goal).count() == 1

    goal_schema.movement_id = db_goal.movement_id
    goal_schema.round_id = 2
    with pytest.raises(exceptions.UnknownRound):
        goal_crud.update_goal(db, goal_schema, db_goal.id)
    assert db.query(goal.Goal).count() == 1


def test_get_goal_by_id(db, db_goal):
    assert db.query(goal.Goal).count() == 1

    wanted_goal = goal_crud.get_goal_by_id(db, db_goal.id)
    assert wanted_goal.id == db_goal.id

    with pytest.raises(exceptions.UnknownMovement):
        goal_crud.get_goal_by_id(db, 2)


def test_delete_goal_by_id(db, db_goal):
    assert db.query(goal.Goal).count() == 1

    with pytest.raises(exceptions.UnknownMovement):
        goal_crud.delete_goal_by_id(db, 2)

    assert goal_crud.delete_goal_by_id(db, db_goal.id)
    assert db.query(goal.Goal).count() == 0
