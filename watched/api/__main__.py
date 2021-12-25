import logging

from aiohttp import web

logger = logging.getLogger(__name__)


def create_app() -> web.Application:
    logger.setLevel(logging.INFO)
    app = web.Application()
    return app


def main():
    app = create_app()
    logger.info('starting application')
    web.run_app(app, host='localhost', port=8080)
    logger.info('application stopped')
