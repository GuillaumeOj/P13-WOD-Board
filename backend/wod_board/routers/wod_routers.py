import typing

import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import user_crud
from wod_board.crud import wod_crud
from wod_board.models import get_db
from wod_board.models import wod
from wod_board.schemas import wod_schemas


router = fastapi.APIRouter(prefix=f"{config.API_URL}/wod", tags=["wod"])


@router.get(
    "/types/{name}", response_model=typing.List[typing.Optional[wod_schemas.WodType]]
)
async def get_wod_types_by_name(
    name: str,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> typing.List[typing.Optional[wod.WodType]]:
    return wod_crud.get_wod_types_by_name(db, name)


@router.post("/", response_model=wod_schemas.Wod)
async def create_wod(
    wod_data: wod_schemas.WodCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> wod.Wod:
    try:
        return wod_crud.create_wod(db, wod_data)
    except wod_crud.UnknownWodType:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This WOD Type doesn't exist",
        )
    except wod_crud.TitleAlreadyUsed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This title is already used",
        )
    except user_crud.UnknownUser:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This author is unknown",
        )


@router.put("/{id}", response_model=wod_schemas.Wod)
async def update_wod(
    wod_data: wod_schemas.WodCreate,
    id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> wod.Wod:
    try:
        return wod_crud.update_wod(db, wod_data, id)
    except wod_crud.UnknownWodType:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This WOD Type doesn't exist",
        )
    except wod_crud.UnknownWod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This WOD doesn't exist",
        )
    except wod_crud.TitleAlreadyUsed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This title is already used",
        )
    except user_crud.UnknownUser:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This author is unknown",
        )


@router.get("/{id}", response_model=wod_schemas.Wod)
async def get_wod_by_id(
    id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> wod.Wod:
    try:
        return wod_crud.get_wod_by_id(db, id)
    except wod_crud.UnknownWod:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This WOD doesn't exist",
        )
