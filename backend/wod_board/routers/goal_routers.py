import typing

import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board.crud import goal_crud
from wod_board.models import get_db
from wod_board.models import goal
from wod_board.schemas import goal_schemas


router = fastapi.APIRouter(prefix=f"{config.API_URL}/goal", tags=["goal"])


@router.post("/", response_model=goal_schemas.Goal)
async def create_goal(
    goal_data: goal_schemas.GoalCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> goal.Goal:
    try:
        return goal_crud.create_goal(db, goal_data)
    except exceptions.UnknownRound:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This round doesn't exist",
        )
    except exceptions.UnknownMovement:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This goal doesn't exist",
        )


@router.put("/{goal_id}", response_model=goal_schemas.Goal)
async def update_goal(
    goal_data: goal_schemas.GoalCreate,
    goal_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> goal.Goal:
    try:
        return goal_crud.update_goal(db, goal_data, goal_id)
    except exceptions.UnknownGoal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This goal doesn't exist",
        )
    except exceptions.UnknownMovement:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This movement doesn't exist",
        )
    except exceptions.UnknownRound:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This round doesn't exist",
        )


@router.get("/{goal_id}", response_model=goal_schemas.Goal)
async def get_goal_by_id(
    goal_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> goal.Goal:
    try:
        return goal_crud.get_goal_by_id(db, goal_id)
    except exceptions.UnknownMovement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This goal doesn't exist",
        )


@router.delete("/{goal_id}")
async def delete_goal_by_id(
    goal_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> typing.Dict["str", "str"]:
    try:
        goal_crud.delete_goal_by_id(db, goal_id)
    except exceptions.UnknownMovement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This goal doesn't exist",
        )

    return {"detail": "Goal successfully deleted"}
