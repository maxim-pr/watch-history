from aiohttp import web

from ..base import BaseHandler
from ...models import WatchEventShow


class AddShowHandler(BaseHandler):

    async def post(self) -> web.Response:
        request_data = await self.request.json()
        show = WatchEventShow(
            user_id=self.user_id,
            **request_data
        )
        await self.watch_history_service.add_show(show)
        return web.Response(status=web.HTTPCreated.status_code)
