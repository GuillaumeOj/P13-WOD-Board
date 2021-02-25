import typing

from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy.orm

from wod_board.crud import user as user_crud
from wod_board.models import get_db
from wod_board.models import user as user_models
from wod_board.schemas import user as user_schemas


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
async def register(
    user: user_schemas.UserCreate, db: sqlalchemy.orm.Session = Depends(get_db)
) -> user_models.User:
    try:
        return user_crud.create_user(db, user)
    except user_crud.DuplicatedEmail:
        raise HTTPException(status_code=400, detail="Email already registered")
    except user_crud.DuplicatedUsername:
        raise HTTPException(status_code=400, detail="Username already registered")
    except RuntimeError:
        raise HTTPException(
            status_code=400, detail="Unexcpected error, please try again"
        )


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> typing.Dict[str, str]:
    pass
