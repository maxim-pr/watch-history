from aiohttp import web

from ..base import BaseHandler

FILTER_QUERY_PARAMS = ('only_films', 'only_shows', 'in_progress', 'finished')


class GetHandler(BaseHandler):

    async def get(self) -> tuple[str, int]:
        watch_history = await self.watch_history_service.get(
            self.user_id, dict()
        )
        return watch_history.json(), web.HTTPOk.status_code
