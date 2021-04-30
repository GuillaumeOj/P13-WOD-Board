# Used for self-referencing models
# See https://pydantic-docs.helpmanual.io/usage/postponed_annotations
from __future__ import annotations

import datetime
import typing

from wod_board.schemas import OrmBase


class WodBase(OrmBase):
    title: str
    description: typing.Optional[str]
    date: datetime.datetime = datetime.datetime.utcnow()
    is_complete: bool = False
    author_id: int
    wod_type_id: typing.Optional[int]


class WodCreate(WodBase):
    pass


class Wod(WodBase):
    id: int
    wod_type: typing.Optional[WodType]
    rounds: "typing.List[Round]"


class WodTypeBase(OrmBase):
    name: str


class WodTypeCreate(WodTypeBase):
    pass


class WodType(WodTypeBase):
    id: int


from wod_board.schemas.round_schemas import Round  # noqa


WodCreate.update_forward_refs()
Wod.update_forward_refs()
