import typing

import pydantic

from wod_board.schemas import OrmBase
from wod_board.schemas import unit_schemas


class EquipmentBase(OrmBase):
    name: str = pydantic.Field(..., max_length=250)
    unit_id: typing.Optional[int]


class EquipmentCreate(EquipmentBase):
    pass


class Equipment(EquipmentBase):
    id: int

    unit: typing.Optional[unit_schemas.Unit]
