import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import movement_crud
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
    return movement_crud.create_movement_goal(db, movement_data)


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


@router.get("/{name}", response_model=movement_schemas.Movement)
async def get_movement_by_exact_name(
    name: str,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> movement.Movement:
    try:
        return movement_crud.get_movement_by_exact_name(db, name)
    except movement_crud.UnknownMovement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{name} doesn't exist yet",
        )