import logging

from aiohttp import web

from ..config import read_config

logger = logging.getLogger(__name__)


def create_app() -> web.Application:
    app = web.Application()
    return app


def main():
    app = create_app()
    config = read_config()
    logger.setLevel(config.log_level)
    logger.info('application started')
    web.run_app(app, host=config.api.host, port=config.api.port)
    logger.info('application stopped')
