import logging

from aiohttp import web

from .handlers import register_views
from .config import Config, read_config
from .logger import setup_logger

logger = logging.getLogger(__name__)


def create_app(config: Config) -> web.Application:
    setup_logger(config.log_level)
    app = web.Application()
    register_views(app)
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
