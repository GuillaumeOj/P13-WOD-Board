from fastapi import FastAPI

from wod_board.routers import user
from wod_board.routers import wod


app = FastAPI()
app.include_router(user.router_user)
app.include_router(user.router_token)
app.include_router(wod.router)
