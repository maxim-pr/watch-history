from typing import Callable

from aiohttp import web


@web.middleware
async def json_middleware(request: web.Request,
                          handler: Callable) -> web.Response:
    status_code, payload = await handler(request)
    if status_code >= 400:
        text = ('{', f'"error": {payload}', '}')
    else:
        text = ('{', f'"data": {payload}', '}')

    return web.json_response(text=''.join(text), status=status_code)
