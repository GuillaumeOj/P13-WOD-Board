import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board import exceptions_routers
from wod_board.crud import wod_crud
from wod_board.models import get_db
from wod_board.models import user
from wod_board.models import wod
from wod_board.schemas import wod_schemas
from wod_board.utils import user_utils


router = fastapi.APIRouter(prefix=f"{config.API_URL}/wod", tags=["wod"])


@router.post("/", response_model=wod_schemas.Wod)
async def create_wod(
    wod_data: wod_schemas.WodCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user.User = fastapi.Depends(user_utils.get_user_with_token),
) -> wod.Wod:
    if wod_data.author_id != current_user.id:
        raise exceptions_routers.AuthorNotUser

    try:
        return wod_crud.create_wod(db, wod_data)
    except exceptions.UnknownWodType:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This WOD Type doesn't exist",
        )
    except exceptions.TitleAlreadyUsed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This title is already used",
        )


@router.put("/{wod_id}", response_model=wod_schemas.Wod)
async def update_wod(
    wod_data: wod_schemas.WodCreate,
    wod_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user.User = fastapi.Depends(user_utils.get_user_with_token),
) -> wod.Wod:
    if wod_data.author_id != current_user.id:
        raise exceptions_routers.AuthorNotUser

    try:
        return wod_crud.update_wod(db, wod_data, wod_id)
    except exceptions.UnknownWodType:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This WOD Type doesn't exist",
        )
    except exceptions.UnknownWod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This WOD doesn't exist",
        )
    except exceptions.TitleAlreadyUsed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This title is already used",
        )


@router.get("/{wod_id}", response_model=wod_schemas.Wod)
async def get_wod_by_id(
    wod_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> wod.Wod:
    try:
        return wod_crud.get_wod_by_id(db, wod_id)
    except exceptions.UnknownWod:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This WOD doesn't exist",
        )
