import logging
from functools import partial

from aiohttp import web
from configargparse import Namespace

from watched.api import register_handlers, MIDDLEWARES
from watched.domain import Service
from watched.logger import setup_logger
from watched.storage import Storage

logger = logging.getLogger(__name__)


async def setup_storage(app: web.Application, db_url: str):
    app['storage'] = Storage(db_url)
    yield
    await app['storage'].close()


async def setup_service(app: web.Application):
    app['service'] = Service(app['storage'])


def create_app(args: Namespace) -> web.Application:
    setup_logger(args.log_level)
    app = web.Application(middlewares=MIDDLEWARES)
    register_handlers(app.router)
    app.cleanup_ctx.append(partial(setup_storage, db_url=args.db_url))
    app.on_startup.append(setup_service)
    return app
