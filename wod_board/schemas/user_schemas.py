import typing

from fastapi import Form
from pydantic import BaseModel
from pydantic import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: typing.Optional[str] = "bearer"


class TokenData(Token):
    email: typing.Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    username: typing.Optional[str]
    first_name: typing.Optional[str]
    last_name: typing.Optional[str]


class UserCreate(UserBase):
    password: str

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(...),
        username: typing.Optional[str] = Form(None),
        first_name: typing.Optional[str] = Form(None),
        last_name: typing.Optional[str] = Form(None),
        password: str = Form(...),
    ) -> "UserCreate":
        return cls(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )


class UserSchema(UserBase):
    id: int

    class Config:
        orm_mode = True
