import pytest


@pytest.mark.asyncio
async def test_add(client):
    response = await client.post("/wod/add", json={})

    assert response.status_code == 200
    assert response.json() == {"details": "Done"}
