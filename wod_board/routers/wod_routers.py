import typing

import fastapi
from fastapi.exceptions import HTTPException
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import wod_crud
from wod_board.models import get_db
from wod_board.schemas import wod_schemas


router = fastapi.APIRouter(prefix=f"{config.API_URL}/wod", tags=["wod"])


@router.post("/add", response_model=wod_schemas.Wod)
async def add_wod(
    wod_data: wod_schemas.WodCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> wod_schemas.Wod:
    return wod_crud.create_wod(db, wod_data)


@router.post("/add/rounds", response_model=typing.List[wod_schemas.Round])
async def add_rounds(
    rounds: typing.List[wod_schemas.RoundCreate],
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> typing.List[wod_schemas.Round]:
    try:
        new_rounds = wod_crud.create_rounds(db, rounds)
    except wod_crud.DuplicatedRoundPosition:
        raise HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Rounds have the same position",
        )

    return new_rounds
