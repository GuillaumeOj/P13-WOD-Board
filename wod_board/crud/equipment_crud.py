import sqlalchemy.orm

from wod_board.models import equipment
from wod_board.schemas import equipment_schemas


class UnknownEquipment(Exception):
    pass


def _create_equipment(
    db: sqlalchemy.orm.Session,
    equiment_schema: equipment_schemas.EquipmentCreate,
) -> equipment.Equipment:
    new_equipment = equipment.Equipment(**equiment_schema.dict())
    db.add(new_equipment)

    db.commit()
    db.refresh(new_equipment)

    return new_equipment


def _get_equipment_by_exact_name(
    db: sqlalchemy.orm.Session,
    wanted_equipment: equipment_schemas.EquipmentCreate,
) -> equipment.Equipment:
    db_equiment: equipment.Equipment = (
        db.query(equipment.Equipment)
        .filter(equipment.Equipment.name == wanted_equipment.name)
        .first()
    )

    if db_equiment is None:
        raise UnknownEquipment

    return db_equiment


def get_or_create_equipment(
    db: sqlalchemy.orm.Session,
    wanted_equipment: equipment_schemas.EquipmentCreate,
) -> equipment_schemas.Equipment:
    try:
        db_equiment = _get_equipment_by_exact_name(db, wanted_equipment)
    except UnknownEquipment:
        db_equiment = _create_equipment(db, wanted_equipment)

    return equipment_schemas.Equipment.from_orm(db_equiment)
