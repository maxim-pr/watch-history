from aiohttp import web

from .add_film import AddFilmHandler
from .add_show import AddShowHandler
from .get import GetWatchHistoryHandler

PREFIX = '/watch_history'


def register_watch_history_handlers(router: web.UrlDispatcher):
    router.add_view(f'{PREFIX}/add_film', AddFilmHandler)
    router.add_view(f'{PREFIX}/add_show', AddShowHandler)
    router.add_view(f'{PREFIX}', GetWatchHistoryHandler)

