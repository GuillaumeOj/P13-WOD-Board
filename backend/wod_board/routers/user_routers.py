from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import user_crud
from wod_board.models import get_db
from wod_board.models import user
from wod_board.schemas import user_schemas
from wod_board.utils import user_utils


router_token = APIRouter(prefix=f"{config.API_URL}", tags=["user"])
router_user = APIRouter(prefix=f"{config.API_URL}/user", tags=["user"])


@router_user.post("/register", response_model=user_schemas.UserSchema)
async def register(
    user_data: user_schemas.UserCreate = Depends(user_schemas.UserCreate.as_form),
    db: sqlalchemy.orm.Session = Depends(get_db),
) -> user.User:
    try:
        new_user = user_crud.create_user(db, user_data)
    except user_crud.DuplicatedEmail:
        error = [
            {"msg": "Email already used"},
        ]
        raise HTTPException(status_code=400, detail=error)
    except user_crud.DuplicatedUsername:
        error = [
            {"msg": "Username already used"},
        ]
        raise HTTPException(status_code=400, detail=error)
    except RuntimeError:
        error = [
            {"msg": "Unexcpected error, please try again"},
        ]
        raise HTTPException(status_code=400, detail=error)

    return new_user


@router_token.post(f"/{config.ACCESS_TOKEN_URL}", response_model=user_schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: sqlalchemy.orm.Session = Depends(get_db),
) -> user_schemas.Token:
    db_user = user_utils.authenticate_user(db, form_data.username, form_data.password)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_utils.create_access_token(user_account=db_user)


@router_user.get("/current", response_model=user_schemas.UserSchema)
async def get_current_user(
    db: sqlalchemy.orm.Session = Depends(get_db),
    user_token: str = Depends(user_utils.OAUTH2_SCHEME),
) -> user.User:
    token = user_schemas.Token(access_token=user_token)

    db_user = user_utils.get_user_with_token(db, token)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return db_user
