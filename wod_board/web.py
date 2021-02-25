from fastapi import FastAPI

from wod_board.routers import user


app = FastAPI()
app.include_router(user.router)
