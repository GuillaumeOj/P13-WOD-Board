import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import movement_crud
from wod_board.crud import round_crud
from wod_board.models import get_db
from wod_board.models import movement
from wod_board.schemas import movement_schemas


router = fastapi.APIRouter(prefix=f"{config.API_URL}/movement", tags=["movement"])


@router.post("/", response_model=movement_schemas.Movement)
async def add_movement(
    movement_data: movement_schemas.MovementCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> movement.Movement:
    return movement_crud.get_or_create_movement(db, movement_data)


@router.post("/goal", response_model=movement_schemas.MovementGoal)
async def add_movement_goal(
    movement_data: movement_schemas.MovementGoalCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> movement.MovementGoal:
    try:
        return movement_crud.create_movement_goal(db, movement_data)
    except round_crud.UnknownRound:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This round doesn't exist",
        )
    except movement_crud.UnknownMovement:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This goal doesn't exist",
        )


@router.put("/goal/{id}", response_model=movement_schemas.MovementGoal)
async def update_movement_goal(
    movement_data: movement_schemas.MovementGoalCreate,
    id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> movement.MovementGoal:
    try:
        return movement_crud.update_movement_goal(db, movement_data, id)
    except movement_crud.UnknownGoal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This goal doesn't exist",
        )
    except movement_crud.UnknownMovement:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This movement doesn't exist",
        )
    except round_crud.UnknownRound:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This round doesn't exist",
        )


@router.get("/goal/{id}", response_model=movement_schemas.MovementGoal)
async def get_movement_goal_by_id(
    id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> movement.MovementGoal:
    try:
        return movement_crud.get_movement_goal_by_id(db, id)
    except movement_crud.UnknownMovement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This goal doesn't exist yet",
        )
