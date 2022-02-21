import json
import logging
from typing import Callable

from aiohttp import web
from pydantic import ValidationError

logger = logging.getLogger(__name__)


@web.middleware
async def errors_middleware(request: web.Request,
                            handler: Callable) -> web.Response:
    try:
        return await handler(request)
    except json.JSONDecodeError as e:
        logger.info(e)
        return web.Response(status=web.HTTPBadRequest.status_code)
    except ValidationError as e:
        logger.info(e)
        return web.Response(status=web.HTTPBadRequest.status_code)
    except web.HTTPClientError as e:
        raise e
    except Exception as e:
        logger.exception(e)
        return web.Response(status=web.HTTPInternalServerError.status_code)
