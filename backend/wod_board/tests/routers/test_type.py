import pytest

from wod_board.models import w_type
from wod_board.schemas import type_schemas


@pytest.mark.asyncio
async def test_create_wod_type(db, client, token):
    assert db.query(w_type.WodType).count() == 0

    type_json = {"name": "AMRAP"}
    response = await client.post(
        "/api/type/",
        json=type_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    excpected_response = type_json | {"id": 1}
    assert response.status_code == 200
    assert response.json() == excpected_response
    assert db.query(w_type.WodType).count() == 1

    response = await client.post(
        "/api/type/",
        json=type_json,
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert db.query(w_type.WodType).count() == 1

    response = await client.post(
        "/api/type/",
        json=type_json,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "This type already exists"}
    assert db.query(w_type.WodType).count() == 1


@pytest.mark.asyncio
async def test_get_wod_types_by_name(db, client):
    response = await client.get("/api/type/list/AMRAP")
    assert response.status_code == 200
    assert response.json() == []

    db.add(w_type.WodType(name="For Time"))
    db.add(w_type.WodType(name="For Load"))
    db.commit()

    response = await client.get("/api/type/list/for")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = await client.get("/api/type/list/loa")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_type_by_id(db, client, db_type):
    assert db.query(w_type.WodType).count() == 1

    response = await client.get(f"/api/type/{db_type.id}")
    assert response.status_code == 200
    assert response.json() == type_schemas.WodType.from_orm(db_type).dict(by_alias=True)

    response = await client.get("/api/type/2")
    assert response.status_code == 422
    assert response.json() == {"detail": "This type doesn't exist"}
