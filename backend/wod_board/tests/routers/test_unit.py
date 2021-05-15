import pytest

from wod_board.models import unit
from wod_board.schemas import unit_schemas


@pytest.mark.asyncio
async def test_create_unit(db, client, token, token_admin):
    assert db.query(unit.Unit).count() == 0

    unit_json = {"name": "Kilograms", "symbol": "kg"}
    response = await client.post(
        "/api/unit/",
        json=unit_json,
        headers={"Authorization": f"Bearer {token_admin.access_token}"},
    )
    expected_response = {
        "id": 1,
        "name": "Kilograms",
        "symbol": "kg",
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(unit.Unit).count() == 1

    response = await client.post("/api/unit/", json=unit_json)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert db.query(unit.Unit).count() == 1

    response = await client.post(
        "/api/unit/",
        json=unit_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Need admin rights"}
    assert db.query(unit.Unit).count() == 1


@pytest.mark.asyncio
async def test_get_unit_by_exact_name(db, client, db_unit):
    assert db.query(unit.Unit).count() == 1

    response = await client.get(f"/api/unit/{db_unit.name}")
    expected_response = unit_schemas.Unit.from_orm(db_unit).dict(by_alias=True)
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(unit.Unit).count() == 1

    response = await client.get("/api/unit/Kilograms")
    assert response.status_code == 422
    assert response.json() == {"detail": "This unit doesn't exist"}
    assert db.query(unit.Unit).count() == 1
