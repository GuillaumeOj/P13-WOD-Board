import pytest

from wod_board import exceptions
from wod_board.crud import movement_crud
from wod_board.models import movement
from wod_board.models import unit
from wod_board.schemas import movement_schemas


def test_create_movement(db):
    unit_unit = unit.Unit(name="Unit", symbol="u")
    db.add(unit_unit)
    db.commit()
    db.refresh(unit_unit)

    assert db.query(movement.Movement).count() == 0

    devil_press = movement_schemas.MovementCreate(
        name="Devil Press", unit_id=unit_unit.id
    )

    assert movement_crud.create_movement(db, devil_press)
    assert db.query(movement.Movement).count() == 1

    devil_press = movement_schemas.MovementCreate(name="Burpees", unit_id=2)
    with pytest.raises(exceptions.UnknownUnit):
        movement_crud.create_movement(db, devil_press)


def test_get_movement_by_id(db):
    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.get_movement_by_id(db, 1)

    unit_unit = unit.Unit(name="Unit", symbol="u")
    db.add(unit_unit)
    db.commit()
    db.refresh(unit_unit)

    devil_press = movement_schemas.MovementCreate(
        name="Devil Press", unit_id=unit_unit.id
    )
    db.add(movement.Movement(name=devil_press.name))
    db.commit()

    assert movement_crud.get_movement_by_id(db, 1)


def test_get_movement_by_name(db):
    db.add(movement.Movement(name="Devil Press"))
    db.commit()

    devil_press = movement_crud.get_movement_by_name(db, "Devil Press")
    assert devil_press.name == devil_press.name

    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.get_movement_by_name(db, "Burpee")

    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.get_movement_by_name(db, "Devil press")


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


def test_get_movements_by_name(db):
    devil_press = movement.Movement(name="Devil Press")
    push_press = movement.Movement(name="Push Press")
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


def test_create_movement_goal(db, db_round):
    deadlift = movement.Movement(name="Dead Lift")
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


def test_update_movement_goal(db, db_round):
    db_deadlift = movement.Movement(name="Dead Lift")
    db.add(db_deadlift)
    db.commit()
    db.refresh(db_deadlift)

    db_movement_goal = movement.MovementGoal(
        movement_id=db_deadlift.id, round_id=db_round.id
    )
    db.add(db_movement_goal)
    db.commit()
    db.refresh(db_movement_goal)

    updated_deadlift_goal = movement_schemas.MovementGoalCreate.from_orm(
        db_movement_goal
    )
    updated_deadlift_goal.repetition = 5

    goal = movement_crud.update_movement_goal(
        db, updated_deadlift_goal, db_movement_goal.id
    )
    assert goal.repetition == updated_deadlift_goal.repetition

    assert db.query(movement.MovementGoal).count() == 1

    with pytest.raises(exceptions.UnknownGoal):
        movement_crud.update_movement_goal(db, updated_deadlift_goal, 2)

    updated_deadlift_goal.movement_id = 2
    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.update_movement_goal(
            db, updated_deadlift_goal, db_movement_goal.id
        )

    updated_deadlift_goal.movement_id = db_movement_goal.movement_id
    updated_deadlift_goal.round_id = 2
    with pytest.raises(exceptions.UnknownRound):
        movement_crud.update_movement_goal(
            db, updated_deadlift_goal, db_movement_goal.id
        )


def test_get_movement_goal_by_id(db):
    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.get_movement_goal_by_id(db, 1)

    devil_press = movement_schemas.MovementCreate(name="Devil Press")
    db_devil_press = movement.Movement(name=devil_press.name)
    db.add(db_devil_press)
    db.commit()
    db.refresh(db_devil_press)

    db.add(movement.MovementGoal(movement=db_devil_press))
    db.commit()

    assert movement_crud.get_movement_goal_by_id(db, 1)


def test_delete_movement_goal_by_id(db, db_round):
    with pytest.raises(exceptions.UnknownMovement):
        movement_crud.delete_movement_goal_by_id(db, 1)

    devil_press = movement.Movement(name="Devil Press")
    goal = movement.MovementGoal(round_id=db_round.id, movement=devil_press)
    db.add(goal)
    db.commit()
    db.refresh(goal)

    assert movement_crud.delete_movement_goal_by_id(db, goal.id)
