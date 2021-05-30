import logging
import os
import typing

import daiquiri
from dotenv import find_dotenv
from dotenv import load_dotenv
from fastapi.security.oauth2 import OAuth2PasswordBearer
from passlib.context import CryptContext

from wod_board.utils import config_utils


load_dotenv(find_dotenv())

WOD_BOARD_ENV: str = config_utils.get_env_or_raise("WOD_BOARD_ENV")

if WOD_BOARD_ENV in ["test", "dev"]:
    LOGGING_LEVEL = logging.INFO
    DEBUG: bool = True
else:
    LOGGING_LEVEL = logging.WARNING
    DEBUG = False

daiquiri.setup(level=LOGGING_LEVEL)

SECRET_KEY: str = config_utils.get_env_or_raise("SECRET_KEY")

if WOD_BOARD_ENV == "test":
    DATABASE_URL: str = "postgresql://wod_board:wod_board@localhost/wod_board_test"
else:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://wod_board:wod_board@localhost/wod_board"
    )

API_URL: str = config_utils.get_env_or_raise("API_URL")
OPEN_API_URL: str = config_utils.get_env_or_raise("OPEN_API_URL")
DOCS_URL: str = config_utils.get_env_or_raise("DOCS_URL")
REDOC_URL: typing.Optional[str] = None
TITLE: str = config_utils.get_env_or_raise("TITLE")
VERSION: str = config_utils.get_env_or_raise("VERSION")

ORIGINS_STR: str = config_utils.get_env_or_raise("ORIGINS")
ORIGINS: typing.List[str] = ORIGINS_STR.split(",")

HASH_SCHEMES: typing.List[str] = ["bcrypt"]

ACCESS_TOKEN_ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
ACCESS_TOKEN_URL: str = "user/token"

PASSWORD_CTXT = CryptContext(schemes=HASH_SCHEMES, deprecated="auto")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=ACCESS_TOKEN_URL)
