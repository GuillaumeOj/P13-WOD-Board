import typing

from fastapi import Form
import pydantic
from pydantic import EmailStr
from pydantic import validator

from wod_board import config
from wod_board.schemas import Base


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserBase(Base):
    email: EmailStr
    username: str
    first_name: typing.Optional[str]
    last_name: typing.Optional[str]
    is_admin: typing.Optional[bool] = False


class UserCreate(UserBase):
    password: str

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(...),
        username: str = Form(...),
        firstName: typing.Optional[str] = Form(None),
        lastName: typing.Optional[str] = Form(None),
        password: str = Form(...),
    ) -> "UserCreate":
        return cls(
            email=email,
            username=username,
            first_name=firstName,
            last_name=lastName,
            password=password,
        )

    @validator("password", pre=True, whole=True)
    def hashed_password(cls, v):
        if isinstance(v, str):
            return config.PASSWORD_CTXT.hash(v)
        return v


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
