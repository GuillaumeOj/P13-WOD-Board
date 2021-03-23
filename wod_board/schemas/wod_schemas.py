# Used for self-referencing models
# See https://pydantic-docs.helpmanual.io/usage/postponed_annotations
from __future__ import annotations

import datetime
import typing

from pydantic import BaseModel


class Wod(BaseModel):
    description: typing.Optional[str]
    note: typing.Optional[str]
    date: datetime.datetime = datetime.datetime.utcnow()

    rounds: typing.List[Round] = []
    wod_type: WodType


class WodType(BaseModel):
    name: str


class Round(BaseModel):
    position: int
    duration_seconds: typing.Optional[int]


Wod.update_forward_refs()
