import typing

from fastapi import APIRouter
from fastapi import Depends
import sqlalchemy.orm

from wod_board.models import get_db


router = APIRouter(prefix="/wod", tags=["wod"])


@router.post("/add")
async def add(db: sqlalchemy.orm.Session = Depends(get_db)) -> typing.Dict[str, str]:
    return {"details": "Done"}
