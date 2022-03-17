from unittest.mock import AsyncMock

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from watched.models import WatchHistoryShowRecord
from .conftest import USER_ID

SHOW_ID = '1'
SHOW_NAME = 'Friends'
RECORD_ID = '2'


def setup_watch_history_repo_stub(app: web.Application):
    repo = app['repos']['watch_history']
    repo.add_show = AsyncMock()
    repo.add_show.return_value = SHOW_ID
    repo.get_prev_show_record = AsyncMock()
    repo.get_prev_show_record.return_value = WatchHistoryShowRecord(
        id='1', user_id=USER_ID, datetime='2021-03-17T02:05:10.632472',
        show_id=SHOW_ID, show_name=SHOW_NAME, season=1, first_episode=1
    )
    repo.add_show_record = AsyncMock()
    repo.add_show_record.return_value = RECORD_ID


request_jsons = [
    {'show_name': SHOW_NAME, 'season': 1, 'first_episode': 2},
    {'show_name': SHOW_NAME, 'season': 1, 'first_episode': 2, 'last_episode': 8},
    {'show_name': SHOW_NAME, 'season': 1, 'finished_season': True},
    {'show_name': SHOW_NAME, 'finished_show': True},
    {'show_id': SHOW_ID, 'season': 1, 'first_episode': 2},
    {'show_id': SHOW_ID, 'season': 1, 'first_episode': 2, 'last_episode': 8},
]


@pytest.mark.parametrize('request_json', request_jsons)
async def test_add_show_record_2xx(client: TestClient, request_json: dict):
    setup_watch_history_repo_stub(client.app)

    response = await client.post('/watch_history/shows', json=request_json)
    response_json = await response.json()

    assert response.status == 201
    assert response_json == {'data': {'id': RECORD_ID}}


request_jsons = [
    {'show_id': SHOW_ID},
    {'show_id': SHOW_ID, 'season': 1, 'first_episode': 2, 'last_episode': 1},
    {'show_id': SHOW_ID, 'finished_season': True},
    {'show_id': SHOW_ID, 'season': 1}
]


@pytest.mark.parametrize('request_json', request_jsons)
async def test_add_show_record_4xx(client: TestClient, request_json: dict):
    response = await client.post('/watch_history/shows', json=request_json)

    assert response.status == 400
