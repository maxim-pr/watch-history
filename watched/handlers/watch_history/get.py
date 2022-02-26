from aiohttp import web

from ..base import BaseHandler
from ...models import WatchHistoryTypeFilter, WatchHistoryStatusFilter


class GetWatchHistoryHandler(BaseHandler):

    async def get(self) -> tuple[int, str]:
        try:
            type_filter, status_filter = self._validate_filters()
        except ValueError:
            raise web.HTTPBadRequest()

        watch_history = await self.watch_history_service.get_watch_history(
            self.user_id, type_filter, status_filter
        )
        return web.HTTPOk.status_code, watch_history.json()

    def _validate_filters(self) -> tuple[WatchHistoryTypeFilter,
                                         WatchHistoryStatusFilter]:
        type_filter = WatchHistoryTypeFilter.ALL
        status_filter = WatchHistoryStatusFilter.ALL

        if self.request.query.get('type') is not None:
            type_filter = WatchHistoryTypeFilter(self.request.query['type'])
        if self.request.query.get('status'):
            status_filter = WatchHistoryStatusFilter(self.request.query['status'])

        return type_filter, status_filter
