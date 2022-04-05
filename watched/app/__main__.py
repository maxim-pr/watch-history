import logging

from aiohttp import web

from .app import create_app

logger = logging.getLogger(__name__)


def main():
    app = create_app()
    logger.info('starting application')
    web.run_app(app, host=app['api_config'].host, port=app['api_config'].port)
    logger.info('application stopped')


if __name__ == '__main__':
    main()
