import logging

from aiohttp import web

from ..base import BaseHandler
from ...models import WatchHistoryFilmRecord, WatchHistoryShowRecord
from ...services.watch_history import RecordDoesNotExistError

logger = logging.getLogger(__name__)


class UpdateFilmRecordHandler(BaseHandler):

    async def put(self) -> web.Response:
        record_id = self.request.match_info['id']
        request_data = await self.request.json()
        film = WatchHistoryFilmRecord(
            id=record_id,
            user_id=self.user_id,
            **request_data
        )

        try:
            await self.watch_history_service.update_film(film)
        except RecordDoesNotExistError as e:
            logger.info(e)
            return web.HTTPNotFound()

        return web.Response(status=web.HTTPNoContent.status_code)


class UpdateShowRecordHandler(BaseHandler):

    async def put(self) -> web.Response:
        record_id = self.request.match_info['id']
        request_data = await self.request.json()
        show = WatchHistoryShowRecord(
            id=record_id,
            user_id=self.user_id,
            **request_data
        )

        try:
            await self.watch_history_service.update_show(show)
        except RecordDoesNotExistError as e:
            logger.info(e)
            return web.HTTPNotFound()

        return web.Response(status=web.HTTPNoContent.status_code)
