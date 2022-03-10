from unittest.mock import Mock, AsyncMock

import pytest
from aiohttp import CookieJar
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from watched.handlers import register_handlers
from watched.middlewares import logging_middleware, errors_middleware, \
    auth_middleware

SESSION_ID = '123'
USER_ID = '123'


def setup_stub_services(app: web.Application):
    users_service = Mock()
    users_service.get_user_id = AsyncMock()
    users_service.get_user_id.return_value = USER_ID

    services = dict()
    services['users'] = users_service
    services['watch_history'] = Mock()
    app['services'] = services


def create_app() -> web.Application:
    app = web.Application(middlewares=[logging_middleware, errors_middleware,
                                       auth_middleware])
    setup_stub_services(app)
    register_handlers(app.router)
    return app


@pytest.fixture
async def client() -> TestClient:
    app = create_app()
    cookie_jar = CookieJar(unsafe=True,
                           treat_as_secure_origin="http://localhost:8080")
    cookie_jar.update_cookies({'session_id': SESSION_ID})
    client_ = TestClient(TestServer(app), cookie_jar=cookie_jar)
    await client_.start_server()
    try:
        yield client_
    finally:
        await client_.close()
