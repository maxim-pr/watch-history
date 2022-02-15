import logging
from typing import Callable

from aiohttp import web

logger = logging.getLogger(__name__)


def error_middleware(request: web.Request, handler: Callable) -> web.Response:
    try:
        response = await handler(request)
    except Exception as e:
        logger.exception(e)
    else:
        return response
