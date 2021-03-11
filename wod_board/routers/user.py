from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy.orm

from wod_board import config
from wod_board.crud import user as user_crud
from wod_board.models import get_db
from wod_board.schemas import user as user_schemas
from wod_board.utils import user as user_utils


router_token = APIRouter(tags=["user"])
router_user = APIRouter(prefix="/user", tags=["user"])


@router_user.post("/register", response_model=user_schemas.User)
async def register(
    user: user_schemas.UserCreate, db: sqlalchemy.orm.Session = Depends(get_db)
) -> user_schemas.User:
    try:
        new_user = user_crud.create_user(db, user)
    except user_crud.DuplicatedEmail:
        raise HTTPException(status_code=400, detail="Email already registered")
    except user_crud.DuplicatedUsername:
        raise HTTPException(status_code=400, detail="Username already registered")
    except RuntimeError:
        raise HTTPException(
            status_code=400, detail="Unexcpected error, please try again"
        )

    return user_schemas.User(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
    )


@router_token.post(f"/{config.ACCESS_TOKEN_URL}", response_model=user_schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: sqlalchemy.orm.Session = Depends(get_db),
) -> user_schemas.Token:
    user = user_utils.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = user_utils.create_access_token(data={"sub": user.email})

    return user_schemas.Token(access_token=access_token, token_type="bearer")
