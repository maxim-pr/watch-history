import json

from aiohttp import web

from ..base import BaseHandler
from ...models import WatchHistoryFilmRecord


class AddFilmHandler(BaseHandler):

    async def post(self) -> tuple[int, str]:
        request_data = await self.request.json()
        film = WatchHistoryFilmRecord(
            user_id=self.user_id,
            **request_data
        )
        watch_event_id, watched_id = await self.watch_history_service.add_film(film)

        data = {
            'watch_event_id': watch_event_id,
            'watched_id': watched_id
        }
        return web.HTTPCreated.status_code, json.dumps(data)
