from typing import Callable

from aiohttp import web

from .. import services


@web.middleware
async def auth_middleware(request: web.Request,
                          handler: Callable) -> web.Response:
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        try:
            user_id = await request.app['services']['users'].get_user_id(session_id)
        except services.users.InvalidUserSession:
            raise web.HTTPUnauthorized()
        else:
            request['user_id'] = user_id

    return await handler(request)
