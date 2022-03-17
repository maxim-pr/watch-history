import logging
from functools import partial

from aiohttp import web
from aioredis import Redis
from sqlalchemy.ext.asyncio import create_async_engine

from .config import DBConfig, RedisConfig, read_config
from .handlers import register_handlers
from .logger import setup_logger
from .middlewares import logging_middleware, auth_middleware, \
    errors_middleware
from .repositories.user_sessions import UserSessionsRepository
from .repositories.watch_history import WatchHistoryRepository
from .services.users import UsersService
from .services.watch_history import WatchHistoryService

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


async def create_repos(app: web.Application):
    repos = dict()
    repos['user_sessions'] = UserSessionsRepository(app['redis'])
    repos['watch_history'] = WatchHistoryRepository(app['db_engine'])
    app['repos'] = repos


async def create_services(app: web.Application):
    services = dict()
    services['users'] = UsersService(app['repos']['user_sessions'])
    services['watch_history'] = WatchHistoryService(
        app['repos']['watch_history']
    )
    app['services'] = services


def create_app() -> web.Application:
    config = read_config()
    setup_logger(config.log_level)
    app = web.Application(middlewares=[logging_middleware, errors_middleware,
                                       auth_middleware])
    app.cleanup_ctx.append(partial(setup_db_engine, db_config=config.db))
    app.cleanup_ctx.append(partial(setup_redis, redis_config=config.redis))
    app.on_startup.append(create_repos)
    app.on_startup.append(create_services)
    register_handlers(app.router)
    return app


def main():
    app = create_app()
    logger.info('starting application')
    web.run_app(app, host='0.0.0.0', port=8080)
    logger.info('application stopped')


if __name__ == '__main__':
    main()
