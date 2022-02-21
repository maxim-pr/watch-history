from aiohttp import web

from ..base import BaseHandler


class GetHandler(BaseHandler):

    async def get(self) -> tuple[str, int]:
        watch_history = await self.watch_history_service.get(self.user_id)
        return watch_history.json(), web.HTTPOk.status_code

