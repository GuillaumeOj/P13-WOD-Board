import fastapi
from fastapi import status
from fastapi.exceptions import HTTPException
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board.crud import equipment_crud
from wod_board.models import get_db
from wod_board.schemas import equipment_schemas


router = fastapi.APIRouter(prefix=f"{config.API_URL}/equipment", tags=["equipment"])


@router.post("/", response_model=equipment_schemas.Equipment)
async def add_equipment(
    equipment_data: equipment_schemas.EquipmentCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> equipment_schemas.Equipment:
    return equipment_schemas.Equipment.from_orm(
        equipment_crud.get_or_create_equipment(db, equipment_data)
    )


@router.get("/{name}")
async def get_equipment_by_exact_name(
    name: str,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> equipment_schemas.Equipment:
    try:
        return equipment_schemas.Equipment.from_orm(
            equipment_crud.get_equipment_by_exact_name(db, name)
        )
    except exceptions.UnknownEquipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{name} doesn't exist yet",
        )
