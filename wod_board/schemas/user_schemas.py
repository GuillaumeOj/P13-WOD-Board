import typing

from pydantic import BaseModel
from pydantic import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: typing.Optional[str] = "bearer"


class TokenData(Token):
    email: typing.Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    username: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int

    class Config:
        orm_mode = True