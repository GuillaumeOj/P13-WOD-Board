import typing

import pydantic

from wod_board.schemas import OrmBase


class EquipmentBase(OrmBase):
    name: str = pydantic.Field(..., max_length=250)
    unit_id: typing.Optional[int] = None


class EquipmentCreate(EquipmentBase):
    pass


class Equipment(EquipmentBase):
    id: int
