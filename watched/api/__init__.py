from .handlers import register_handlers
from .middlewares import (
    auth_middleware, logging_middleware,
    encoding_middleware, errors_middleware
)

MIDDLEWARES = [auth_middleware, logging_middleware,
               encoding_middleware, errors_middleware]


__all__ = ['register_handlers', 'MIDDLEWARES']
