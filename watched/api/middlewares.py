import json
import logging
from datetime import datetime
from enum import Enum
from typing import Callable, Any, Optional

from aiohttp import web
from pydantic import ValidationError

logger = logging.getLogger(__name__)


@web.middleware
async def auth_middleware(request: web.Request,
                          handler: Callable) -> web.Response:
    if 'User-ID' not in request.headers:
        logger.error('non-authorized access')
        return web.HTTPUnauthorized()
    return await handler(request)


@web.middleware
async def logging_middleware(request: web.Request,
                             handler: Callable) -> web.Response:
    response = await handler(request)

    log_message = ' '.join(
        [f'method={request.method}',
         f'uri={request.path}',
         f'status={response.status}',
         f'user_id={request.headers["User-ID"]}']
    )
    if response.status >= 500:
        logger.error(log_message)
    else:
        logger.info(log_message)

    return response


class Encoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


@web.middleware
async def encoding_middleware(request: web.Request,
                              handler: Callable) -> web.Response:
    status, data = await handler(request)
    if data is not None:
        if status < 400:
            data = {'data': data}
        else:
            data = {'error': data}
        encoded_data = json.dumps(data, cls=Encoder)
        return web.Response(body=encoded_data, status=status,
                            content_type='application/json')
    return web.Response(status=status)


@web.middleware
async def errors_middleware(request: web.Request,
                            handler: Callable) -> tuple[int, Optional[dict]]:
    try:
        return await handler(request)
    except json.JSONDecodeError:
        return web.HTTPBadRequest.status_code, None
    except ValidationError as e:
        logger.info(e)
        data = {'message': 'invalid request data'}
        return web.HTTPBadRequest.status_code, data
    except web.HTTPError as e:
        return e.status_code, None
    except Exception as e:
        logger.exception(e, exc_info=True)
        return web.HTTPInternalServerError.status_code, None
