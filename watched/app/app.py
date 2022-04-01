import logging
from functools import partial

from aiohttp import web

from watched.api.handlers import register_handlers
from watched.api.middlewares import encoding_middleware, errors_middleware, \
    logging_middleware
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
    app = web.Application(middlewares=[logging_middleware, errors_middleware,
                                       encoding_middleware])
    register_handlers(app.router)
    app.cleanup_ctx.append(partial(setup_storage, db_config=config.db))
    app.on_startup.append(setup_service)
    app['api_config'] = config.api
    return app


def main():
    app = create_app()
    logger.info('starting application')
    web.run_app(app, host=app['api_config'].host, port=app['api_config'].port)
    logger.info('application stopped')


if __name__ == '__main__':
    main()
