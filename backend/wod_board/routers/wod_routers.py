import typing

import daiquiri
import fastapi
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board.crud import wod_crud
from wod_board.models import get_db
from wod_board.models import user
from wod_board.models import wod
from wod_board.schemas import wod_schemas
from wod_board.utils import user_utils


LOG = daiquiri.getLogger(__name__)


router = fastapi.APIRouter(prefix=f"{config.API_URL}/wod", tags=["wod"])


@router.post("/", response_model=wod_schemas.Wod)
async def create_wod(
    wod_data: wod_schemas.WodCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user.User = fastapi.Depends(user_utils.get_user_with_token),
) -> wod.Wod:
    if wod_data.author_id != current_user.id:
        error = exceptions.UserIsNotAuthor(current_user.username)
        LOG.error(error)
        raise exceptions.RouterException(error)

    try:
        return wod_crud.create_wod(db, wod_data)
    except exceptions.UnknownWodType as error:
        raise exceptions.RouterException(error)
    except exceptions.TitleAlreadyUsed as error:
        raise exceptions.RouterException(error)


@router.get("/incomplete", response_model=wod_schemas.Wod)
async def get_wod_incomplete(
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user.User = fastapi.Depends(user_utils.get_user_with_token),
) -> typing.Optional[wod.Wod]:
    try:
        return wod_crud.get_wod_incomplete(db, current_user.id)
    except exceptions.UnknownWod:
        return None


@router.put("/{wod_id}", response_model=wod_schemas.Wod)
async def update_wod(
    wod_data: wod_schemas.WodCreate,
    wod_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user.User = fastapi.Depends(user_utils.get_user_with_token),
) -> wod.Wod:
    if wod_data.author_id != current_user.id:
        error = exceptions.UserIsNotAuthor(current_user.username)
        LOG.error(error)
        raise exceptions.RouterException(error)

    try:
        return wod_crud.update_wod(db, wod_data, wod_id)
    except exceptions.UnknownWodType as error:
        raise exceptions.RouterException(error)
    except exceptions.UnknownWod as error:
        raise exceptions.RouterException(error)
    except exceptions.TitleAlreadyUsed as error:
        raise exceptions.RouterException(error)


@router.get("/{wod_id}", response_model=wod_schemas.Wod)
async def get_wod_by_id(
    wod_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> wod.Wod:
    try:
        return wod_crud.get_wod_by_id(db, wod_id)
    except exceptions.UnknownWod as error:
        raise exceptions.RouterException(error)
