from aiohttp import web

from ..base import BaseHandler
from ...models import WatchEventFilm


class AddFilmHandler(BaseHandler):

    async def post(self) -> web.Response:
        request_data = await self.request.json()
        film = WatchEventFilm(
            user_id=self.user_id,
            **request_data
        )
        await self.watch_history_service.add_film(film)
        return web.Response(status=web.HTTPCreated.status_code)
