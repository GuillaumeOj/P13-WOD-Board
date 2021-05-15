import typing

import daiquiri
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import exceptions
from wod_board.models import goal
from wod_board.schemas import goal_schemas
from wod_board.utils import goal_utils


LOG = daiquiri.getLogger(__name__)


def create_goal(
    db: sqlalchemy.orm.Session,
    goal_data: goal_schemas.GoalCreate,
    user_id: int,
) -> goal.Goal:
    goal_utils.check_goal_author(db, goal_data.round_id, user_id)

    new_goal = goal.Goal(
        movement_id=goal_data.movement_id,
        round_id=goal_data.round_id,
        repetition=goal_data.repetition,
        duration_seconds=goal_data.duration_seconds,
    )
    db.add(new_goal)

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if (
            'insert or update on table "goal" violates foreign '
            'key constraint "goal_movement_id_fkey"'
        ) in str(error):
            raise exceptions.UnknownMovement(str(goal_data.movement_id))

        LOG.error(str(error))

    db.refresh(new_goal)

    return new_goal


def update_goal(
    db: sqlalchemy.orm.Session,
    goal_data: goal_schemas.GoalCreate,
    goal_id: int,
    user_id: int,
) -> goal.Goal:
    db_goal: typing.Optional[goal.Goal] = db.get(goal.Goal, goal_id)

    if db_goal is None:
        raise exceptions.UnknownGoal(str(goal_id))

    goal_utils.check_goal_author(db, goal_data.round_id, user_id)

    db_goal.movement_id = goal_data.movement_id
    db_goal.round_id = goal_data.round_id
    db_goal.repetition = goal_data.repetition
    db_goal.duration_seconds = goal_data.duration_seconds

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        db.rollback()
        if (
            'insert or update on table "goal" violates foreign '
            'key constraint "goal_movement_id_fkey"'
        ) in str(error):
            raise exceptions.UnknownMovement(str(goal_data.movement_id))

        LOG.error(str(error))

    db.refresh(db_goal)

    return db_goal


def get_goal_by_id(db: sqlalchemy.orm.Session, goal_id: int) -> goal.Goal:
    db_goal: goal.Goal = db.get(goal.Goal, goal_id)

    if db_goal is None:
        raise exceptions.UnknownGoal(str(goal_id))

    return db_goal


def delete_goal_by_id(
    db: sqlalchemy.orm.Session, goal_id: int, user_id: int
) -> typing.Literal[True]:
    db_goal: typing.Optional[goal.Goal] = db.get(goal.Goal, goal_id)

    if db_goal is None:
        raise exceptions.UnknownGoal(str(goal_id))

    goal_utils.check_goal_author(db, db_goal.round_id, user_id)

    db.delete(db_goal)
    db.commit()

    return True
