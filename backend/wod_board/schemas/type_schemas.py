# Used for self-referencing models
# See https://pydantic-docs.helpmanual.io/usage/postponed_annotations
from __future__ import annotations

from wod_board.schemas import OrmBase


class WodTypeBase(OrmBase):
    name: str


class WodTypeCreate(WodTypeBase):
    pass


class WodType(WodTypeBase):
    id: int
