import typing

import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board.crud import round_crud
from wod_board.models import get_db
from wod_board.models import wod_round
from wod_board.schemas import round_schemas
from wod_board.schemas import user_schemas
from wod_board.utils import user_utils


router = fastapi.APIRouter(prefix=f"{config.API_URL}/round", tags=["round"])


@router.post("/", response_model=round_schemas.Round)
async def create_round(
    round_data: round_schemas.RoundCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user_schemas.User = fastapi.Depends(user_utils.get_user_with_token),
) -> wod_round.Round:
    try:
        return round_crud.create_round(db, round_data, current_user.id)
    except exceptions.DuplicatedRoundPosition:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Rounds have the same position",
        )
    except exceptions.UnknownWod:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The given WOD id is unknown",
        )
    except exceptions.UserIsNotAuthor:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Author don't match with authenticated user",
        )


@router.put("/{round_id}", response_model=round_schemas.Round)
async def update_round(
    round_data: round_schemas.RoundCreate,
    round_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user_schemas.User = fastapi.Depends(user_utils.get_user_with_token),
) -> wod_round.Round:
    try:
        return round_crud.update_round(db, round_data, round_id, current_user.id)
    except exceptions.DuplicatedRoundPosition:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Rounds have the same position",
        )
    except exceptions.UnknownWod:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The given WOD id is unknown",
        )
    except exceptions.UnknownRound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This round doesn't exist",
        )
    except exceptions.UserIsNotAuthor:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Author don't match with authenticated user",
        )


@router.delete("/{round_id}")
async def delete_round_by_id(
    round_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user_schemas.User = fastapi.Depends(user_utils.get_user_with_token),
) -> typing.Dict[str, str]:
    try:
        round_crud.delete_round_by_id(db, round_id, current_user.id)
    except exceptions.UnknownRound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This round doesn't exist",
        )
    except exceptions.UserIsNotAuthor:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Author don't match with authenticated user",
        )

    return {"detail": "Round successfully deleted"}
