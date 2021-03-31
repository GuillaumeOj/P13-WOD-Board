from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import wod_crud
from wod_board.models import get_db
from wod_board.schemas import wod_schemas


router = APIRouter(prefix=f"{config.API_URL}/wod", tags=["wod"])


@router.post("/add", response_model=wod_schemas.Wod)
async def add(
    wod_data: wod_schemas.WodCreate, db: sqlalchemy.orm.Session = Depends(get_db)
) -> wod_schemas.Wod:
    try:
        new_wod = wod_crud.create_wod(db, wod_data)
    except wod_crud.DuplicatedRoundPosition:
        raise HTTPException(status_code=400, detail="Rounds have the same position")

    return new_wod
