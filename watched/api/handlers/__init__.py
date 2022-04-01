from aiohttp import web

from .add import AddFilmRecordHandler, AddShowRecordHandler
from .update import UpdateFilmRecordHandler

PREFIX = '/api'


def register_handlers(router: web.UrlDispatcher):
    router.add_view(PREFIX + '/films', AddFilmRecordHandler)
    router.add_view(PREFIX + '/shows', AddShowRecordHandler)
    router.add_view(PREFIX + '/films/{id}', UpdateFilmRecordHandler)
