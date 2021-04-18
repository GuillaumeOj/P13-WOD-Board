import pytest

from wod_board.models import unit


@pytest.mark.asyncio
async def test_add(db, client):
    unit_json = {"name": "Kilograms", "symbol": "kg"}
    response = await client.post("/api/unit/", json=unit_json)

    expected_response = {
        "id": 1,
        "name": "Kilograms",
        "symbol": "kg",
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_unit_by_exact_name(db, client):
    name = "Kilograms"
    response = await client.get(f"/api/unit/{name}")

    expected_response = {"detail": f"{name} doesn't exist yet"}

    assert response.status_code == 404
    assert response.json() == expected_response

    wanted_unit = unit.Unit(name=name, symbol="kg")
    db.add(wanted_unit)
    db.commit()

    response = await client.get(f"/api/unit/{name}")

    expected_response = {
        "id": 1,
        "name": "Kilograms",
        "symbol": "kg",
    }

    assert response.status_code == 200
    assert response.json() == expected_response
