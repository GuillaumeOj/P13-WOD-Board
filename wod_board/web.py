from fastapi import FastAPI
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from wod_board import config
from wod_board.routers import equipment_routers
from wod_board.routers import movement_routers
from wod_board.routers import round_routers
from wod_board.routers import unit_routers
from wod_board.routers import user_routers
from wod_board.routers import wod_routers


app = FastAPI(docs_url=f"{config.API_URL}/docs", redoc_url=None)
app.include_router(equipment_routers.router)
app.include_router(movement_routers.router)
app.include_router(round_routers.router)
app.include_router(unit_routers.router)
app.include_router(user_routers.router_user)
app.include_router(user_routers.router_token)
app.include_router(wod_routers.router)

sentry_sdk.init(
    dsn="https://9ab3f6551b3549c993c01dcb041bb41d@o453278.ingest.sentry.io/5704632",
    traces_sample_rate=1.0,
)
app.add_middleware(SentryAsgiMiddleware)
