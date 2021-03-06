import typing

import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board.crud import type_crud
from wod_board.models import get_db
from wod_board.models import w_type
from wod_board.schemas import type_schemas
from wod_board.utils import user_utils


router = fastapi.APIRouter(prefix=f"{config.API_URL}/type", tags=["type"])


@router.get(
    "/list/{name}", response_model=typing.List[typing.Optional[type_schemas.WodType]]
)
async def get_wod_types_by_name(
    name: str,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> typing.List[typing.Optional[w_type.WodType]]:
    return type_crud.get_wod_types_by_name(db, name)


@router.post(
    "/",
    response_model=type_schemas.WodType,
    dependencies=[fastapi.Depends(user_utils.get_user_with_token)],
)
async def create_wod_type(
    wod_type: type_schemas.WodTypeCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> w_type.WodType:
    try:
        return type_crud.create_wod_type(db, wod_type)
    except exceptions.NameAlreadyUsed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This type already exists",
        )
