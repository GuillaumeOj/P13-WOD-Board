import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import wod_crud
from wod_board.models import get_db
from wod_board.schemas import wod_schemas


router = fastapi.APIRouter(prefix=f"{config.API_URL}/wod", tags=["wod"])


@router.post("/", response_model=wod_schemas.Wod)
async def add_wod(
    wod_data: wod_schemas.WodCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> wod_schemas.Wod:
    return wod_schemas.Wod.from_orm(wod_crud.create_wod(db, wod_data))


@router.get("/{id}", response_model=wod_schemas.Wod)
async def get_wod_by_id(
    id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> wod_schemas.Wod:
    try:
        return wod_schemas.Wod.from_orm(wod_crud.get_wod_by_id(db, id))
    except wod_crud.UnknownWod:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This WOD doesn't exist",
        )