import logging
from typing import Callable

from aiohttp import web

from ..services.users import InvalidUserSession

logger = logging.getLogger(__name__)


@web.middleware
async def auth_middleware(request: web.Request,
                          handler: Callable) -> web.Response:
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        try:
            user_id = await request.app['services']['users'].\
                get_user_id(session_id)
        except InvalidUserSession as e:
            logger.info(e)
            return web.HTTPUnauthorized()
        else:
            request['user_id'] = user_id

    return await handler(request)
