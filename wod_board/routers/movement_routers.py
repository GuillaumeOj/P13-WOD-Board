import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import movement_crud
from wod_board.models import get_db
from wod_board.schemas import movement_schemas


router = fastapi.APIRouter(prefix=f"{config.API_URL}/movement", tags=["movement"])


@router.post("/", response_model=movement_schemas.Movement)
async def add_movement(
    movement_data: movement_schemas.MovementCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> movement_schemas.Movement:
    return movement_schemas.Movement.from_orm(
        movement_crud.get_or_create_movement(db, movement_data)
    )


@router.get("/{name}")
async def get_movement_by_exact_name(
    name: str,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> movement_schemas.Movement:
    try:
        return movement_schemas.Movement.from_orm(
            movement_crud.get_movement_by_exact_name(db, name)
        )
    except movement_crud.UnknownMovement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{name} doesn't exist yet",
        )
