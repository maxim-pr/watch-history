from aiohttp import web

from .base import BaseHandler
from ..dto import GetWatchHistoryDTO


class GetWatchHistoryHandler(BaseHandler):
    async def get(self) -> tuple[int, dict]:
        dto = GetWatchHistoryDTO(
            user_id=self.user_id,
            type_filter=self.request.query.get('type'),
            status_filter=self.request.query.get('status')
        )

        watch_history = await self.service.get_watch_history(dto)

        response_data = {
            'data': watch_history.dict()['__root__']
        }
        return web.HTTPOk.status_code, response_data
