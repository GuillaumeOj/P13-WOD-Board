from fastapi import FastAPI

from wod_board.routers import user_routers
from wod_board.routers import wod_routers


app = FastAPI()
app.include_router(user_routers.router_user)
app.include_router(user_routers.router_token)
app.include_router(wod_routers.router)
