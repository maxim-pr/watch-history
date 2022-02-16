import logging

from aiohttp import web

from ..base import BaseHandler
from ...models import watch_history

logger = logging.getLogger(__name__)


class AddFilm(BaseHandler):

    async def post(self) -> web.Response:
        request_data = await self.request.json()
        film = watch_history.Film(
            user_id=self.user_id,
            **request_data,
            is_show=False
        )
        await self.watch_history_service.add_film(film)
        return web.Response(status=web.HTTPCreated.status_code)
