import pytest

from wod_board.models import equipment


@pytest.mark.asyncio
async def test_add(db, client):
    equipment_json = {"name": "Dumbbel"}
    response = await client.post("/api/equipment/", json=equipment_json)

    expected_response = {
        "id": 1,
        "name": "Dumbbel",
        "unit_id": None,
        "unit": None,
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_unit_by_exact_name(db, client):
    name = "Dumbbel"
    response = await client.get(f"/api/equipment/{name}")

    expected_response = {"detail": f"{name} doesn't exist yet"}

    assert response.status_code == 404
    assert response.json() == expected_response

    wanted_equipment = equipment.Equipment(name=name, unit_id=None)
    db.add(wanted_equipment)
    db.commit()

    response = await client.get(f"/api/equipment/{name}")

    expected_response = {
        "id": 1,
        "name": "Dumbbel",
        "unit_id": None,
        "unit": None,
    }

    assert response.status_code == 200
    assert response.json() == expected_response
