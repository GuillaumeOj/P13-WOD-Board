import daiquiri
import fastapi
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board.crud import unit_crud
from wod_board.models import get_db
from wod_board.models import unit
from wod_board.models import user
from wod_board.schemas import unit_schemas
from wod_board.utils import user_utils


LOG = daiquiri.getLogger(__name__)


router = fastapi.APIRouter(prefix=f"{config.API_URL}/unit", tags=["unit"])


@router.get("/{name}", response_model=unit_schemas.Unit)
async def get_unit_by_name(
    name: str,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> unit.Unit:
    try:
        return unit_crud.get_unit_by_name(db, name)
    except exceptions.UnknownUnit as error:
        raise exceptions.RouterException(error)


@router.post("/", response_model=unit_schemas.Unit)
async def create_unit(
    unit_data: unit_schemas.UnitCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
    current_user: user.User = fastapi.Depends(user_utils.get_user_with_token),
) -> unit.Unit:
    if not current_user.is_admin:
        error = exceptions.UserIsNotAdmin(current_user.username)
        LOG.error(error)
        raise exceptions.RouterException(error)

    return unit_crud.get_or_create_unit(db, unit_data)
