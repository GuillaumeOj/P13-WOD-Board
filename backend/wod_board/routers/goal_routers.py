import typing

import fastapi
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board.crud import goal_crud
from wod_board.models import get_db
from wod_board.models import goal
from wod_board.schemas import goal_schemas
from wod_board.schemas import user_schemas
from wod_board.utils import user_utils


router = fastapi.APIRouter(prefix=f"{config.API_URL}/goal", tags=["goal"])


@router.post("/", response_model=goal_schemas.Goal)
async def create_goal(
    goal_data: goal_schemas.GoalCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user_schemas.User = fastapi.Depends(user_utils.get_user_with_token),
) -> goal.Goal:
    try:
        return goal_crud.create_goal(db, goal_data, current_user.id)
    except exceptions.UnknownMovement as error:
        raise exceptions.RouterException(error)
    except exceptions.UnknownRound as error:
        raise exceptions.RouterException(error)
    except exceptions.UserIsNotAuthor as error:
        raise exceptions.RouterException(error)


@router.put("/{goal_id}", response_model=goal_schemas.Goal)
async def update_goal(
    goal_data: goal_schemas.GoalCreate,
    goal_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user_schemas.User = fastapi.Depends(user_utils.get_user_with_token),
) -> goal.Goal:
    try:
        return goal_crud.update_goal(db, goal_data, goal_id, current_user.id)
    except exceptions.UnknownGoal as error:
        raise exceptions.RouterException(error)
    except exceptions.UnknownMovement as error:
        raise exceptions.RouterException(error)
    except exceptions.UnknownRound as error:
        raise exceptions.RouterException(error)
    except exceptions.UserIsNotAuthor as error:
        raise exceptions.RouterException(error)


@router.get("/{goal_id}", response_model=goal_schemas.Goal)
async def get_goal_by_id(
    goal_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> goal.Goal:
    try:
        return goal_crud.get_goal_by_id(db, goal_id)
    except exceptions.UnknownGoal as error:
        raise exceptions.RouterException(error)


@router.delete("/{goal_id}")
async def delete_goal_by_id(
    goal_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user_schemas.User = fastapi.Depends(user_utils.get_user_with_token),
) -> typing.Dict["str", "str"]:
    try:
        goal_crud.delete_goal_by_id(db, goal_id, current_user.id)
    except exceptions.UnknownGoal as error:
        raise exceptions.RouterException(error)
    except exceptions.UserIsNotAuthor as error:
        raise exceptions.RouterException(error)

    return {"detail": "Goal successfully deleted"}
