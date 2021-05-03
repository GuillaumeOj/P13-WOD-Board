import pytest

from wod_board.models import unit


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
