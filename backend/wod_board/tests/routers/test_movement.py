import pytest

from wod_board.models import movement
from wod_board.schemas import movement_schemas


@pytest.mark.asyncio
async def test_create_movement(db, client, db_unit, token):
    assert db.query(movement.Movement).count() == 0

    movement_json = {"name": "Devil Press", "unitId": db_unit.id}
    response = await client.post(
        "/api/movement/",
        json=movement_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    expected_response = movement_json | {
        "id": 1,
        "unit": {
            "id": db_unit.id,
            "name": db_unit.name,
            "symbol": db_unit.symbol,
        },
        "equipments": [],
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(movement.Movement).count() == 1


@pytest.mark.asyncio
async def test_get_movements_by_name(db, client, db_unit):
    devil_press = movement.Movement(name="Devil Press", unit_id=db_unit.id)
    push_press = movement.Movement(name="Push Press", unit_id=db_unit.id)
    db.add_all([devil_press, push_press])
    db.commit()
    db.refresh(devil_press)
    db.refresh(push_press)

    response = await client.get("/api/movement/movements/Pres")
    expected_response = [
        movement_schemas.Movement.from_orm(devil_press).dict(by_alias=True),
        movement_schemas.Movement.from_orm(push_press).dict(by_alias=True),
    ]
    assert response.status_code == 200
    assert response.json() == expected_response

    response = await client.get("/api/movement/movements/Devil Pres")
    expected_response = [
        movement_schemas.Movement.from_orm(devil_press).dict(by_alias=True),
    ]
    assert response.status_code == 200
    assert response.json() == expected_response

    response = await client.get("/api/movement/movements/Burpee")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_movement_by_id(db, client, db_movement):
    assert db.query(movement.Movement).count() == 1

    response = await client.get(f"/api/movement/{db_movement.id}")
    assert response.status_code == 200
    assert response.json() == movement_schemas.Movement.from_orm(db_movement).dict(
        by_alias=True
    )

    response = await client.get(f"/api/movement/{db_movement.id + 1}")
    assert response.status_code == 422
    assert response.json() == {"detail": "This movement doesn't exist"}
