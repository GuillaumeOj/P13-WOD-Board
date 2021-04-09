import pydantic

from wod_board.schemas import OrmBase


class UnitBase(OrmBase):
    name: str = pydantic.Field(..., max_length=250)
    symbol: str = pydantic.Field(..., to_lower=True, max_length=5)


class UnitCreate(UnitBase):
    pass


class Unit(UnitBase):
    id: int
