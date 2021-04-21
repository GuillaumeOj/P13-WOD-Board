import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.exc
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import round_crud
from wod_board.models import get_db
from wod_board.models import wod_round
from wod_board.schemas import round_schemas


router = fastapi.APIRouter(prefix=f"{config.API_URL}/round", tags=["round"])


@router.post("/", response_model=round_schemas.Round)
async def add_round(
    round_data: round_schemas.RoundCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> wod_round.Round:
    try:
        return round_crud.create_round(db, round_data)
    except round_crud.DuplicatedRoundPosition:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Rounds have the same position",
        )
    except round_crud.WrongWodId:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The given WOD id is unknown",
        )


@router.put("/{id}", response_model=round_schemas.Round)
async def update_round(
    round_data: round_schemas.RoundCreate,
    id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> wod_round.Round:
    try:
        return round_crud.update_round(db, round_data, id)
    except round_crud.DuplicatedRoundPosition:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Rounds have the same position",
        )
    except round_crud.WrongWodId:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The given WOD id is unknown",
        )
    except round_crud.UnknownRound:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This round doesn't exist",
        )


@router.get("/{id}", response_model=round_schemas.Round)
async def get_round_by_id(
    id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> wod_round.Round:
    try:
        return round_crud.get_round_by_id(db, id)
    except round_crud.UnknownRound:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unknown round",
        )
