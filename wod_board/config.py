import os
import typing

from dotenv import find_dotenv
from dotenv import load_dotenv


load_dotenv(find_dotenv())

DATABASE_URL: str = os.getenv(
    "DATABASE_URL", "postgresql://wod_board:wod_board@localhost/wod_board:5432"
)
HASH_SCHEMES: typing.List[str] = ["bcrypt"]
ACCESS_TOKEN_ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
ACCESS_TOKEN_URL: str = "login"
SECRET_KEY: str = os.getenv("SECRET_KEY", "foo_key_for_testing_purpose")
