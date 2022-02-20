import logging
from functools import partial

from aiohttp import web
from aioredis import Redis
from sqlalchemy.ext.asyncio import create_async_engine

from .config import Config, DBConfig, RedisConfig, read_config
from .handlers import register_handlers
from .logger import setup_logger
from .middlewares import auth_middleware, error_middleware
from .repositories import UserSessionsRepository, WatchHistoryRepository, \
    WatchedRepository
from .services import UsersService, WatchHistoryService

logger = logging.getLogger(__name__)


async def setup_db_engine(app: web.Application, db_config: DBConfig):
    app['db_engine'] = create_async_engine(
        url=db_config.url,
        echo=db_config.log_sql
    )
    yield
    await app['db_engine'].dispose()


async def setup_redis(app: web.Application, redis_config: RedisConfig):
    app['redis'] = Redis.from_url(redis_config.url)
    yield
    await app['redis'].close()


def setup_repositories(app: web.Application):
    repos = dict()
    repos['user_sessions'] = UserSessionsRepository(app['redis'])
    repos['watch_history'] = WatchHistoryRepository(app['db_engine'])
    repos['watched'] = WatchedRepository(app['db_engine'])
    app['repos'] = repos


async def setup_services(app: web.Application):
    setup_repositories(app)
    services = dict()
    services['users'] = UsersService(app['repos']['user_sessions'])
    services['watch_history'] = WatchHistoryService(
        app['repos']['watch_history'], app['repos']['watched']
    )
    app['services'] = services


def create_app(config: Config) -> web.Application:
    setup_logger(config.log_level)
    app = web.Application(middlewares=[auth_middleware, error_middleware])
    app.cleanup_ctx.append(partial(setup_db_engine, db_config=config.db))
    app.cleanup_ctx.append(partial(setup_redis, redis_config=config.redis))
    app.on_startup.append(setup_services)
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
