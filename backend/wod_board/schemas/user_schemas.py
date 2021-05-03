import typing

from fastapi import Form
from pydantic import BaseModel
from pydantic import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: typing.Optional[str]
    last_name: typing.Optional[str]
    is_admin: bool = False


class UserCreate(UserBase):
    password: str

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(...),
        username: str = Form(...),
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
