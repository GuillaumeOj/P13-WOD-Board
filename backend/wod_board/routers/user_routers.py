import daiquiri
import fastapi
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy.orm

from wod_board import config
from wod_board import exceptions
from wod_board.crud import user_crud
from wod_board.models import get_db
from wod_board.models import user
from wod_board.schemas import user_schemas
from wod_board.utils import user_utils


LOG = daiquiri.getLogger(__name__)


router_token = fastapi.APIRouter(prefix=f"{config.API_URL}", tags=["user"])
router_user = fastapi.APIRouter(prefix=f"{config.API_URL}/user", tags=["user"])


@router_user.post("/register", response_model=user_schemas.User)
async def register(
    user_data: user_schemas.UserCreate = fastapi.Depends(
        user_schemas.UserCreate.as_form
    ),
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> user.User:
    try:
        new_user = user_crud.create_user(db, user_data)
    except exceptions.DuplicatedEmail as error:
        raise exceptions.RouterException(error)
    except exceptions.DuplicatedUsername as error:
        raise exceptions.RouterException(error)

    return new_user


@router_token.post(f"/{config.ACCESS_TOKEN_URL}", response_model=user_schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = fastapi.Depends(),
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
) -> user_schemas.Token:
    login_exception = HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        db_user = user_crud.get_user_by_email(db, form_data.username)
    except exceptions.UnknownUser:
        raise login_exception

    if not config.PASSWORD_CTXT.verify(form_data.password, db_user.password):
        raise login_exception

    return user_utils.create_access_token(db_user)


@router_user.get("/current", response_model=user_schemas.User)
async def get_current_user(
    current_user: user.User = fastapi.Depends(user_utils.get_user_with_token),
) -> user.User:
    return current_user
