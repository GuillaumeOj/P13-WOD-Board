import fastapi
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
