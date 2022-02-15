from aiohttp import web

from .add_watched_film import AddWatchedFilmView


def register_handlers(router: web.UrlDispatcher):
    router.add_view('/add_film', AddWatchedFilmView)

