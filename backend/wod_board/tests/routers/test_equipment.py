import pytest

from wod_board.models import equipment


@pytest.mark.asyncio
async def test_create_equipment(db, client, token):
    assert db.query(equipment.Equipment).count() == 0

    equipment_json = {"name": "Dumbbel"}
    response = await client.post("/api/equipment/", json=equipment_json)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert db.query(equipment.Equipment).count() == 0

    response = await client.post(
        "/api/equipment/",
        json=equipment_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    expected_response = {
        "id": 1,
        "name": "Dumbbel",
        "unitId": None,
        "unit": None,
    }
    assert response.status_code == 200
    assert response.json() == expected_response
    assert db.query(equipment.Equipment).count() == 1


@pytest.mark.asyncio
async def test_get_equipment_by_name(db, client):
    name = "Dumbbel"
    response = await client.get(f"/api/equipment/{name}")
    assert response.status_code == 422
    assert response.json() == {"detail": "This equipment doesn't exist"}

    wanted_equipment = equipment.Equipment(name=name, unit_id=None)
    db.add(wanted_equipment)
    db.commit()
    db.refresh(wanted_equipment)

    response = await client.get(f"/api/equipment/{name}")
    expected_response = {
        "id": 1,
        "name": "Dumbbel",
        "unitId": None,
        "unit": None,
    }
    assert response.status_code == 200
    assert response.json() == expected_response
