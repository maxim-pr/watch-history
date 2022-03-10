from unittest.mock import AsyncMock

from aiohttp.test_utils import TestClient

FILM_RECORD_ID = '1'


async def test_add_film_record(client: TestClient):
    add_film_record = AsyncMock()
    add_film_record.return_value = FILM_RECORD_ID
    client.app['services']['watch_history'].add_film_record = add_film_record

    response = await client.post(
        '/watch_history/films',
        json={
            'film_name': 'Terminal'
        }
    )
    response_json = await response.json()

    assert response.status == 201
    assert response_json == {'data': {'id': FILM_RECORD_ID}}
