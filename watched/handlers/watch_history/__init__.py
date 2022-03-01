from aiohttp import web

from .add import AddFilmToWatchHistory, AddShowToWatchHistory
from .get import GetWatchHistoryHandler

PREFIX = '/watch_history'


def register_watch_history_handlers(router: web.UrlDispatcher):
    router.add_view(f'{PREFIX}', GetWatchHistoryHandler)
    router.add_view(f'{PREFIX}/films', AddFilmToWatchHistory)
    router.add_view(f'{PREFIX}/shows', AddShowToWatchHistory)
