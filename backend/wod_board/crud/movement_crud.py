import daiquiri
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board.crud import round_crud
from wod_board.crud import unit_crud
from wod_board.models import movement
from wod_board.schemas import movement_schemas


LOG = daiquiri.getLogger(__name__)


class UnknownMovement(Exception):
    pass


class UnknownGoal(Exception):
    pass


def create_movement(
    db: sqlalchemy.orm.Session,
    movement_data: movement_schemas.MovementCreate,
) -> movement.Movement:
    new_movement = movement.Movement(
        name=movement_data.name, unit_id=movement_data.unit_id
    )
    db.add(new_movement)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if (
            'insert or update on table "movement" violates foreign '
            'key constraint "movement_unit_id_fkey"'
        ) in str(error):
            raise unit_crud.UnknownUnit

        LOG(str(error))

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


def get_movement_by_name(
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
        db_movement = get_movement_by_name(db, movement_data.name)
    except UnknownMovement:
        db_movement = create_movement(db, movement_data)

    return db_movement


def create_movement_goal(
    db: sqlalchemy.orm.Session,
    goal: movement_schemas.MovementGoalCreate,
) -> movement.MovementGoal:
    new_goal = movement.MovementGoal(
        movement_id=goal.movement_id,
        round_id=goal.round_id,
        repetition=goal.repetition,
        duration_seconds=goal.duration_seconds,
    )
    db.add(new_goal)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if (
            'insert or update on table "movement_goal" violates foreign '
            'key constraint "movement_goal_round_id_fkey"'
        ) in str(error):
            raise round_crud.UnknownRound
        if (
            'insert or update on table "movement_goal" violates foreign '
            'key constraint "movement_goal_movement_id_fkey"'
        ) in str(error):
            raise UnknownMovement

        LOG.error(str(error))

    db.refresh(new_goal)

    return new_goal


def update_movement_goal(
    db: sqlalchemy.orm.Session,
    goal: movement_schemas.MovementGoalCreate,
    id: int,
) -> movement.MovementGoal:
    movement_goal: movement.MovementGoal = db.get(movement.MovementGoal, id)

    if movement_goal is None:
        raise UnknownGoal

    movement_goal.movement_id = goal.movement_id
    movement_goal.round_id = goal.round_id
    movement_goal.repetition = goal.repetition
    movement_goal.duration_seconds = goal.duration_seconds

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if (
            'insert or update on table "movement_goal" violates foreign '
            'key constraint "movement_goal_round_id_fkey"'
        ) in str(error):
            raise round_crud.UnknownRound
        if (
            'insert or update on table "movement_goal" violates foreign '
            'key constraint "movement_goal_movement_id_fkey"'
        ) in str(error):
            raise UnknownMovement

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
