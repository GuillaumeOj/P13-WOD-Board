import typing

import pydantic

from wod_board.schemas import OrmBase
from wod_board.schemas import equipment_schemas


class MovementBase(OrmBase):
    name: str = pydantic.Field(..., max_length=250)
    unit_id: typing.Optional[int] = None


class MovementCreate(MovementBase):
    equipments: typing.Optional[typing.List[equipment_schemas.EquipmentCreate]] = []


class Movement(MovementBase):
    id: int
    equipments: typing.Optional[typing.List[equipment_schemas.Equipment]] = None
