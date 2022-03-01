import logging
from typing import Callable

from aiohttp import web

logger = logging.getLogger(__name__)


@web.middleware
async def logging_middleware(request: web.Request,
                             handler: Callable) -> web.Response:
    response = await handler(request)

    log_message = f'{request.method} {request.path} {response.status}'
    if request.get('user_id') is not None:
        log_message += f' {request["user_id"]}'
    if response.status < 500:
        logger.info(log_message)
    else:
        logger.error(log_message)

    return response
