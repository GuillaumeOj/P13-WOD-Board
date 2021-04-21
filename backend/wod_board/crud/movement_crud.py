import daiquiri
import sqlalchemy.orm

from wod_board.crud import equipment_crud
from wod_board.crud import round_crud
from wod_board.crud import unit_crud
from wod_board.models import movement
from wod_board.schemas import movement_schemas


LOG = daiquiri.getLogger(__name__)


class UnknownMovement(Exception):
    pass


def create_movement(
    db: sqlalchemy.orm.Session,
    movement_data: movement_schemas.MovementCreate,
) -> movement.Movement:
    new_movement = movement.Movement(name=movement_data.name)

    if movement_data.equipments:
        new_movement.equipments = [
            equipment_crud.get_or_create_equipment(db, equipment)
            for equipment in movement_data.equipments
        ]

    if movement_data.unit:
        new_movement.unit = unit_crud.get_or_create_unit(db, movement_data.unit)

    db.add(new_movement)

    db.commit()
    db.refresh(new_movement)

    return new_movement


def get_movement_by_id(
    db: sqlalchemy.orm.Session,
    id: int,
) -> movement.Movement:
    db_movement: movement.Movement = db.get(movement.Movement, id)

    if db_movement is None:
        raise UnknownMovement

    return db_movement


def get_movement_by_exact_name(
    db: sqlalchemy.orm.Session,
    name: str,
) -> movement.Movement:
    db_movement: movement.Movement = (
        db.query(movement.Movement).filter(movement.Movement.name == name).first()
    )

    if db_movement is None:
        raise UnknownMovement

    return db_movement


def get_or_create_movement(
    db: sqlalchemy.orm.Session,
    movement_data: movement_schemas.MovementCreate,
) -> movement.Movement:
    try:
        db_movement = get_movement_by_exact_name(db, movement_data.name)
    except UnknownMovement:
        db_movement = create_movement(db, movement_data)

    return db_movement


def create_movement_goal(
    db: sqlalchemy.orm.Session,
    goal: movement_schemas.MovementGoalCreate,
) -> movement.MovementGoal:
    base_movement = get_or_create_movement(db, goal.movement)

    new_movement = movement.MovementGoal(
        movement=base_movement,
        round_id=goal.round_id,
        repetition=goal.repetition,
    )

    if goal.equipments:
        new_movement.equipments = [
            equipment_crud.get_or_create_equipment(db, equipment)
            for equipment in goal.equipments
        ]

    db.add(new_movement)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()

        if (
            'insert or update on table "movement_goal" violates foreign '
            'key constraint "movement_goal_round_id_fkey"'
        ) in str(error):
            raise round_crud.UnknownRound

        LOG.error(str(error))

    db.refresh(new_movement)

    return new_movement


def update_movement_goal(
    db: sqlalchemy.orm.Session,
    goal: movement_schemas.MovementGoalCreate,
    id: int,
) -> movement.MovementGoal:
    movement_goal: movement.MovementGoal = db.get(movement.MovementGoal, id)

    if movement_goal is None:
        raise UnknownMovement

    base_movement = get_movement_by_exact_name(db, goal.movement.name)

    movement_goal.movement = base_movement
    movement_goal.round_id = goal.round_id
    movement_goal.repetition = goal.repetition

    if goal.equipments:
        movement_goal.equipments = [
            equipment_crud.get_or_create_equipment(db, equipment)
            for equipment in goal.equipments
        ]

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()

        if (
            'insert or update on table "movement_goal" violates foreign '
            'key constraint "movement_goal_round_id_fkey"'
        ) in str(error):
            raise round_crud.UnknownRound

        LOG.error(str(error))

    db.refresh(movement_goal)

    return movement_goal


def get_movement_goal_by_id(
    db: sqlalchemy.orm.Session, id: int
) -> movement.MovementGoal:
    db_movement: movement.MovementGoal = db.get(movement.MovementGoal, id)

    if db_movement is None:
        raise UnknownMovement

    return db_movement
