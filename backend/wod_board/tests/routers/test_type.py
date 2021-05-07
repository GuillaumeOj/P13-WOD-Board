import pytest

from wod_board.models import w_type


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
