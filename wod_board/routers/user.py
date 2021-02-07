import typing

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> typing.Dict[str, str]:
    pass
