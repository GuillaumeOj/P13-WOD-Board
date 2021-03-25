# Used for self-referencing models
# See https://pydantic-docs.helpmanual.io/usage/postponed_annotations
from __future__ import annotations

import datetime
import typing

import pydantic

from wod_board.schemas import OrmBase


class WodBase(OrmBase):
    description: typing.Optional[str]
    note: typing.Optional[str]
    date: datetime.datetime = datetime.datetime.utcnow()


class WodCreate(WodBase):
    rounds: typing.List[RoundCreate]
    wod_type: WodTypeCreate

    @pydantic.validator("rounds", always=True)
    def evaluate_rounds_position(cls, rounds):
        s = set()
        for w_round in rounds:
            if w_round.position in s:
                raise ValueError("duplicated position")
            s.add(w_round.position)

        return rounds


class Wod(WodBase):
    id: int
    wod_type_id: int
    wod_type: WodType
    rounds: typing.List[Round]


class WodTypeBase(OrmBase):
    name: str


class WodTypeCreate(WodTypeBase):
    pass


class WodType(WodTypeBase):
    id: int


class RoundBase(OrmBase):
    position: int
    duration_seconds: int = 0


class RoundCreate(RoundBase):
    pass


class Round(RoundBase):
    id: int
    wod_id: int


WodCreate.update_forward_refs()
Wod.update_forward_refs()
