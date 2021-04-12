import typing

import pydantic

from wod_board.schemas import OrmBase
from wod_board.schemas import equipment_schemas
from wod_board.schemas import unit_schemas


class MovementBase(OrmBase):
    name: str = pydantic.Field(..., max_length=250)
    unit_id: typing.Optional[int]


class MovementCreate(MovementBase):
    unit: typing.Optional[unit_schemas.UnitCreate]
    equipments: typing.Optional[typing.List[equipment_schemas.EquipmentCreate]]


class Movement(MovementBase):
    id: int
    unit: typing.Optional[unit_schemas.Unit]
    equipments: typing.Optional[typing.List[equipment_schemas.Equipment]]
