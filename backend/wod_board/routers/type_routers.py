import typing

import fastapi
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import type_crud
from wod_board.models import get_db
from wod_board.models import w_type
from wod_board.schemas import type_schemas


router = fastapi.APIRouter(prefix=f"{config.API_URL}/type", tags=["type"])


@router.get(
    "/list/{name}", response_model=typing.List[typing.Optional[type_schemas.WodType]]
)
async def get_wod_types_by_name(
    name: str,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> typing.List[typing.Optional[w_type.WodType]]:
    return type_crud.get_wod_types_by_name(db, name)
