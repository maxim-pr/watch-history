import json

from aiohttp import web

from ..base import BaseHandler
from ...models import WatchHistoryFilmRecord, WatchHistoryShowRecord


class AddFilmToWatchHistory(BaseHandler):

    async def post(self) -> tuple[int, str]:
        request_data = await self.request.json()
        film = WatchHistoryFilmRecord(
            user_id=self.user_id,
            **request_data
        )
        watch_history_record_id = await self.watch_history_service.add_film(film)

        data = {
            'id': watch_history_record_id
        }
        return web.HTTPCreated.status_code, json.dumps(data)


class AddShowToWatchHistory(BaseHandler):

    async def post(self) -> tuple[int, str]:
        request_data = await self.request.json()
        show = WatchHistoryShowRecord(
            user_id=self.user_id,
            **request_data
        )
        watch_history_record_id = await self.watch_history_service.add_show(show)

        data = {
            'id': watch_history_record_id
        }
        return web.HTTPCreated.status_code, json.dumps(data)
