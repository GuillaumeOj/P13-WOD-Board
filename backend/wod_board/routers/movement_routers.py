import typing

import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board.crud import movement_crud
from wod_board.models import get_db
from wod_board.models import movement
from wod_board.schemas import movement_schemas
from wod_board.utils import user_utils


router = fastapi.APIRouter(prefix=f"{config.API_URL}/movement", tags=["movement"])


@router.post(
    "/",
    response_model=movement_schemas.Movement,
    dependencies=[
        fastapi.Depends(user_utils.get_user_with_token),
    ],
)
async def create_movement(
    movement_data: movement_schemas.MovementCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> movement.Movement:
    try:
        return movement_crud.create_movement(db, movement_data)
    except exceptions.DuplicatedMovement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This movement already exist",
        )


@router.get(
    "/{name}", response_model=typing.List[typing.Optional[movement_schemas.Movement]]
)
async def get_movements_by_name(
    name: str,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> typing.List[typing.Optional[movement.Movement]]:
    return movement_crud.get_movements_by_name(db, name)
