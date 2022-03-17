from unittest.mock import AsyncMock

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

RECORD_ID = '1'


def setup_watch_history_repo_stub(app: web.Application):
    repo = app['repos']['watch_history']
    repo.find_film_record_by_name = AsyncMock()
    repo.find_film_record_by_name.return_value = None
    repo.add_film_record = AsyncMock()
    repo.add_film_record.return_value = RECORD_ID


request_jsons = [
    {'film_name': 'Terminal'},
    {'film_name': 'Terminal', 'datetime': '2022-03-17T02:05:10.632472'}
]


@pytest.mark.parametrize('request_json', request_jsons)
async def test_add_film_record_2xx(client: TestClient, request_json: dict):
    setup_watch_history_repo_stub(client.app)

    response = await client.post('/watch_history/films', json=request_json)
    response_json = await response.json()

    assert response.status == 201
    assert response_json == {'data': {'id': RECORD_ID}}
