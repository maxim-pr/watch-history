from aiohttp import web

from .watch_history.add_film import AddFilm


def register_handlers(router: web.UrlDispatcher):
    router.add_view('/watch_history/add_film', AddFilm)

