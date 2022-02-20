from aiohttp import web

from .add_film import AddFilmHandler
from .add_show import AddShowHandler

PREFIX = '/watch_history'


def register_watch_history_handlers(router: web.UrlDispatcher):
    router.add_view(f'{PREFIX}/add_film', AddFilmHandler)
    router.add_view(f'{PREFIX}/add_show', AddShowHandler)
