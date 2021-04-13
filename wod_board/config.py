import logging
import os
import typing

from dotenv import find_dotenv
from dotenv import load_dotenv


load_dotenv(find_dotenv())

SECRET_KEY: str = os.getenv("SECRET_KEY", "foo_key_for_testing_purpose")

WOD_BOARD_ENV: typing.Optional[str] = os.getenv("WOD_BOARD_ENV")

if WOD_BOARD_ENV == "test":
    DATABASE_URL: str = "postgresql://wod_board:wod_board@localhost/wod_board_test"
else:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://wod_board:wod_board@localhost/wod_board"
    )

HASH_SCHEMES: typing.List[str] = ["bcrypt"]

ACCESS_TOKEN_ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
ACCESS_TOKEN_URL: str = "user/token"

API_URL: str = os.getenv("API_URL", "/api")

if WOD_BOARD_ENV == "test":
    LOGGING_LEVEL = logging.INFO
else:
    LOGGING_LEVEL = logging.WARNING
