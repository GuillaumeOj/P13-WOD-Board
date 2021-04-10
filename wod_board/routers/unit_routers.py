import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import unit_crud
from wod_board.models import get_db
from wod_board.schemas import unit_schemas


router = fastapi.APIRouter(prefix=f"{config.API_URL}/unit", tags=["unit"])


@router.post("/", response_model=unit_schemas.Unit)
async def add_unit(
    unit_data: unit_schemas.UnitCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> unit_schemas.Unit:
    return unit_schemas.Unit.from_orm(unit_crud.get_or_create_unit(db, unit_data))


@router.get("/{name}")
async def get_unit_by_exact_name(
    name: str,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> unit_schemas.Unit:
    try:
        return unit_schemas.Unit.from_orm(unit_crud.get_unit_by_exact_name(db, name))
    except unit_crud.UnknownUnit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{name} doesn't exist yet",
        )
