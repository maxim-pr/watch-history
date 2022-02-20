from aiohttp import web

from .watch_history import register_watch_history_handlers


def register_handlers(router: web.UrlDispatcher):
    register_watch_history_handlers(router)
