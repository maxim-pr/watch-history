import json
import logging
from datetime import datetime
from enum import Enum
from typing import Callable, Any

from aiohttp import web
from pydantic import ValidationError

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


@web.middleware
async def errors_middleware(request: web.Request,
                            handler: Callable) -> web.Response:
    try:
        return await handler(request)
    except json.JSONDecodeError:
        return web.Response(status=web.HTTPBadRequest.status_code)
    except ValidationError:
        response_data = {
            'error': {
                'message': 'invalid request data'
            }
        }
        return web.json_response(data=response_data,
                                 status=web.HTTPBadRequest.status_code)
    except web.HTTPError as e:
        return e
    except Exception as e:
        logger.exception(e, exc_info=True)
        return web.Response(status=web.HTTPInternalServerError.status_code)


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
        encoded_data = json.dumps(data, cls=Encoder)
        return web.Response(body=encoded_data, status=status,
                            content_type='application/json')
    return web.Response(status=status)
