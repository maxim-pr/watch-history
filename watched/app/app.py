import logging
from functools import partial

from aiohttp import web

from watched.api import register_handlers, MIDDLEWARES
from watched.domain import Service
from watched.logger import setup_logger
from watched.storage import Storage
from .config import DBConfig, read_config

logger = logging.getLogger(__name__)


async def setup_storage(app: web.Application, db_config: DBConfig):
    app['storage'] = Storage(db_config.url, db_config.log_sql)
    yield
    await app['storage'].close()


async def setup_service(app: web.Application):
    app['service'] = Service(app['storage'])


def create_app() -> web.Application:
    config = read_config()
    setup_logger(logging.getLogger('watched'), config.log_level)
    app = web.Application(middlewares=MIDDLEWARES)
    register_handlers(app.router)
    app.cleanup_ctx.append(partial(setup_storage, db_config=config.db))
    app.on_startup.append(setup_service)
    app['api_config'] = config.api
    return app
