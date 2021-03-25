import pytest


@pytest.mark.asyncio
async def test_add(db, client):
    wod_json = {
        "description": "string",
        "note": "string",
        "date": "2021-03-24T14:42:46.580110",
        "rounds": [
            {
                "position": 0,
                "duration_seconds": 0,
            },
        ],
        "wod_type": {
            "name": "string",
        },
    }
    response = await client.post("/wod/add", json=wod_json)

    expected_response = {
        "id": 1,
        "description": "string",
        "note": "string",
        "date": "2021-03-24T14:42:46.580110",
        "rounds": [
            {
                "id": 1,
                "wod_id": 1,
                "position": 0,
                "duration_seconds": 0,
            }
        ],
        "wod_type_id": 1,
        "wod_type": {
            "id": 1,
            "name": "string",
        },
    }

    assert response.status_code == 200
    assert response.json() == expected_response
