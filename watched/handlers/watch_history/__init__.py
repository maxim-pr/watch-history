from aiohttp import web

from .add import AddFilmRecordHandler, AddShowRecordHandler
from .delete import DeleteRecordHandler
from .get import GetWatchHistoryHandler
from .update import UpdateFilmRecordHandler, UpdateShowRecordHandler

PREFIX = '/watch_history'


def register_watch_history_handlers(router: web.UrlDispatcher):
    router.add_get(PREFIX, GetWatchHistoryHandler)
    router.add_post(PREFIX + '/films', AddFilmRecordHandler)
    router.add_post(PREFIX + '/shows', AddShowRecordHandler)
    router.add_put(PREFIX + '/films/{id}', UpdateFilmRecordHandler)
    router.add_put(PREFIX + '/shows/{id}', UpdateShowRecordHandler)
    router.add_delete(PREFIX + '/{id}', DeleteRecordHandler)
