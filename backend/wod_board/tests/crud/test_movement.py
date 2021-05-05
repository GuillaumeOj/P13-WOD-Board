import pytest

from wod_board import exceptions
from wod_board.crud import movement_crud
from wod_board.models import movement
from wod_board.models import unit
from wod_board.schemas import movement_schemas


def test_create_movement(db, db_unit):
    assert db.query(movement.Movement).count() == 0

    devil_press = movement_schemas.MovementCreate(
        name="Devil Press", unit_id=db_unit.id
    )
    assert movement_crud.create_movement(db, devil_press)
    assert db.query(movement.Movement).count() == 1

    with pytest.raises(exceptions.DuplicatedMovement):
        movement_crud.create_movement(db, devil_press)
    assert db.query(movement.Movement).count() == 1

    burpees = movement_schemas.MovementCreate(name="Burpees", unit_id=2)
    with pytest.raises(exceptions.UnknownUnit):
        movement_crud.create_movement(db, burpees)


def test_get_movement_by_id(db, db_movement):
    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.get_movement_by_id(db, 2)

    wanted_movement = movement_crud.get_movement_by_id(db, db_movement.id)
    assert wanted_movement.id == db_movement.id


def test_get_movement_by_name(db, db_movement):
    devil_press = movement_crud.get_movement_by_name(db, db_movement.name)
    assert devil_press.name == devil_press.name

    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.get_movement_by_name(db, "Burpee")

    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.get_movement_by_name(db, db_movement.name.lower())


def test_get_or_create_movement(db):
    unit_unit = unit.Unit(name="Unit", symbol="u")
    db.add(unit_unit)
    db.commit()
    db.refresh(unit_unit)

    assert db.query(movement.Movement).count() == 0

    devil_press = movement_schemas.MovementCreate(
        name="Devil Press", unit_id=unit_unit.id
    )

    assert movement_crud.get_or_create_movement(db, devil_press)
    assert movement_crud.get_or_create_movement(db, devil_press)
    assert db.query(movement.Movement).count() == 1


def test_get_movements_by_name(db, db_unit):
    devil_press = movement.Movement(name="Devil Press", unit_id=db_unit.id)
    push_press = movement.Movement(name="Push Press", unit_id=db_unit.id)
    db.add_all([devil_press, push_press])
    db.commit()
    db.refresh(devil_press)
    db.refresh(push_press)

    movements = movement_crud.get_movements_by_name(db, "pres")
    assert len(movements) == 2

    movements = movement_crud.get_movements_by_name(db, "push pres")
    assert len(movements) == 1
    assert movements[0].name == push_press.name

    movements = movement_crud.get_movements_by_name(db, "Burpee")
    assert movements == []


def test_create_movement_goal(db, db_round, db_unit):
    deadlift = movement.Movement(name="Dead Lift", unit_id=db_unit.id)
    db.add(deadlift)
    db.commit()
    db.refresh(deadlift)

    assert db.query(movement.MovementGoal).count() == 0

    deadlift_goal = movement_schemas.MovementGoalCreate(
        movement_id=deadlift.id,
        round_id=db_round.id,
        repetition=5,
    )
    assert movement_crud.create_movement_goal(db, deadlift_goal)
    assert db.query(movement.MovementGoal).count() == 1

    deadlift_goal = movement_schemas.MovementGoalCreate(
        movement_id=2,
        round_id=db_round.id,
        repetition=5,
    )

    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.create_movement_goal(db, deadlift_goal)

    deadlift_goal = movement_schemas.MovementGoalCreate(
        movement_id=deadlift.id,
        round_id=2,
        repetition=5,
    )

    with pytest.raises(exceptions.UnknownRound):
        movement_crud.create_movement_goal(db, deadlift_goal)


def test_update_movement_goal(db, db_round, db_movement):
    db_goal = movement.MovementGoal(movement_id=db_movement.id, round_id=db_round.id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)

    updated_goal = movement_schemas.MovementGoalCreate.from_orm(db_goal)
    updated_goal.repetition = 5

    goal = movement_crud.update_movement_goal(db, updated_goal, db_goal.id)
    assert goal.repetition == updated_goal.repetition

    assert db.query(movement.MovementGoal).count() == 1

    with pytest.raises(exceptions.UnknownGoal):
        movement_crud.update_movement_goal(db, updated_goal, 2)

    updated_goal.movement_id = 2
    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.update_movement_goal(db, updated_goal, db_goal.id)

    updated_goal.movement_id = db_goal.movement_id
    updated_goal.round_id = 2
    with pytest.raises(exceptions.UnknownRound):
        movement_crud.update_movement_goal(db, updated_goal, db_goal.id)


def test_get_movement_goal_by_id(db, db_goal):
    goal = movement_crud.get_movement_goal_by_id(db, db_goal.id)
    assert goal.id == db_goal.id

    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.get_movement_goal_by_id(db, 2)


def test_delete_movement_goal_by_id(db, db_goal):
    assert db.query(movement.MovementGoal).count() == 1

    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.delete_movement_goal_by_id(db, 2)

    assert movement_crud.delete_movement_goal_by_id(db, db_goal.id)
    assert db.query(movement.MovementGoal).count() == 0
