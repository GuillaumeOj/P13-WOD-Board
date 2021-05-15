import fastapi
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board.crud import equipment_crud
from wod_board.models import equipment
from wod_board.models import get_db
from wod_board.schemas import equipment_schemas
from wod_board.utils import user_utils


router = fastapi.APIRouter(prefix=f"{config.API_URL}/equipment", tags=["equipment"])


@router.post(
    "/",
    response_model=equipment_schemas.Equipment,
    dependencies=[fastapi.Depends(user_utils.get_user_with_token)],
)
async def create_equipment(
    equipment_data: equipment_schemas.EquipmentCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> equipment.Equipment:
    try:
        return equipment_crud.create_equipment(db, equipment_data)
    except exceptions.NameAlreadyUsed as error:
        raise exceptions.RouterException(error)


@router.get("/{name}", response_model=equipment_schemas.Equipment)
async def get_equipment_by_name(
    name: str,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> equipment.Equipment:
    try:
        return equipment_crud.get_equipment_by_name(db, name)
    except exceptions.UnknownEquipment as error:
        raise exceptions.RouterException(error)
