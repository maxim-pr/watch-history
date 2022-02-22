from typing import Callable

from aiohttp import web


@web.middleware
async def json_middleware(request: web.Request,
                          handler: Callable) -> web.Response:
    data, status_code = await handler(request)
    text = ('{', f'"data": {data}', '}')
    return web.json_response(text=''.join(text), status=status_code)
