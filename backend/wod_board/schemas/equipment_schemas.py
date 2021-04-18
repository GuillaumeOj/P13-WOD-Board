import typing

import pydantic

from wod_board.schemas import OrmBase
from wod_board.schemas import unit_schemas


class EquipmentBase(OrmBase):
    name: str = pydantic.Field(..., max_length=250)


class EquipmentCreate(EquipmentBase):
    unit: typing.Optional[unit_schemas.UnitCreate]


class Equipment(EquipmentBase):
    id: int
    unit_id: typing.Optional[int]

    unit: typing.Optional[unit_schemas.Unit]
