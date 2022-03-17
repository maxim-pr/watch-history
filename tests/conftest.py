from unittest.mock import Mock, AsyncMock

import pytest
from aiohttp import CookieJar
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from watched.__main__ import create_services
from watched.handlers import register_handlers
from watched.middlewares import logging_middleware, errors_middleware, \
    auth_middleware

SESSION_ID = '123'
USER_ID = '123'


def create_repos_stubs(app: web.Application):
    repos = dict()
    user_sessions_repo = Mock()
    user_sessions_repo.get_user_id = AsyncMock()
    user_sessions_repo.get_user_id.return_value = USER_ID
    repos['user_sessions'] = user_sessions_repo
    repos['watch_history'] = Mock()
    app['repos'] = repos


async def create_app() -> web.Application:
    app = web.Application(middlewares=[logging_middleware, errors_middleware,
                                       auth_middleware])
    create_repos_stubs(app)
    await create_services(app)
    register_handlers(app.router)
    return app


@pytest.fixture
async def client() -> TestClient:
    app = await create_app()
    cookie_jar = CookieJar(unsafe=True,
                           treat_as_secure_origin="http://localhost:8080")
    cookie_jar.update_cookies({'session_id': SESSION_ID})
    client_ = TestClient(TestServer(app), cookie_jar=cookie_jar)
    await client_.start_server()
    try:
        yield client_
    finally:
        await client_.close()
