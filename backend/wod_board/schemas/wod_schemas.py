# Used for self-referencing models
# See https://pydantic-docs.helpmanual.io/usage/postponed_annotations
from __future__ import annotations

import datetime
import typing

import pydantic

from wod_board.schemas import OrmBase


class WodBase(OrmBase):
    title: str = pydantic.Field(..., max_length=250)
    description: typing.Optional[str] = pydantic.Field(default="", max_length=250)
    date: datetime.datetime = datetime.datetime.utcnow()
    is_complete: bool = False
    author_id: int
    wod_type_id: typing.Optional[int]


class WodCreate(WodBase):
    pass


class Wod(WodBase):
    id: int
    wod_type: "typing.Optional[WodType]"
    rounds: "typing.List[Round]"


from wod_board.schemas.round_schemas import Round  # noqa
from wod_board.schemas.type_schemas import WodType  # noqa


WodCreate.update_forward_refs()
Wod.update_forward_refs()
