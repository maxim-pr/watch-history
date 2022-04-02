from aiohttp import web

from .add import AddFilmRecordHandler, AddShowRecordHandler
from .get import GetWatchHistoryHandler
from .update import UpdateFilmRecordHandler

PREFIX = '/api/watch_history'


def register_handlers(router: web.UrlDispatcher):
    router.add_view(PREFIX, GetWatchHistoryHandler)
    router.add_view(PREFIX + '/films', AddFilmRecordHandler)
    router.add_view(PREFIX + '/shows', AddShowRecordHandler)
    router.add_view(PREFIX + '/films/{id}', UpdateFilmRecordHandler)
