from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from wod_board import config
from wod_board.routers import user


app = FastAPI()

app.include_router(user.router)

oauth2_schema = OAuth2PasswordBearer(tokenUrl=config.TOKEN_URL)

password_ctxt = CryptContext(schemes=config.HASH_SCHEMES, deprecated="auto")
