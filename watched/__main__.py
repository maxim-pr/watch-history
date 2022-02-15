import logging
from functools import partial

from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine

from .config import Config, DBConfig, read_config
from .handlers import register_handlers
from .logger import setup_logger
from .service import Service

logger = logging.getLogger(__name__)


async def setup_db_engine(app: web.Application, db_config: DBConfig):
    app['db_engine'] = create_async_engine(
        url=db_config.url,
        echo=db_config.log_sql
    )
    yield
    await app['db_engine'].dispose()


async def setup_service(app: web.Application):
    app['service'] = Service(app['db_engine'])


def create_app(config: Config) -> web.Application:
    setup_logger(config.log_level)
    app = web.Application()
    app.cleanup_ctx.append(partial(setup_db_engine, db_config=config.db))
    app.on_startup.append(setup_service)
    register_handlers(app.router)
    return app


def main():
    try:
        config = read_config()
    except Exception as e:
        logger.exception(e)
        return

    app = create_app(config)
    logger.info('starting application')
    web.run_app(app, host=config.api.host, port=config.api.port)
    logger.info('application stopped')
