import logging

from aiohttp import web

from .base import BaseView

logger = logging.getLogger(__name__)


class AddWatchedFilmView(BaseView):

    async def post(self) -> web.Response:
        pass
