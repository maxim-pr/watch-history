import json

from aiohttp import web

from ..base import BaseHandler
from ...models import WatchHistoryShowRecord


class AddShowHandler(BaseHandler):

    async def post(self) -> tuple[int, str]:
        request_data = await self.request.json()
        show = WatchHistoryShowRecord(
            user_id=self.user_id,
            **request_data
        )
        if not is_consistent(show):
            raise web.HTTPBadRequest()

        watch_event_id, watched_id = await self.watch_history_service.add_show(show)
        data = {
            'watch_event_id': watch_event_id,
            'watched_id': watched_id
        }
        return web.HTTPCreated.status_code, json.dumps(data)


def is_consistent(show: WatchHistoryShowRecord) -> bool:
    if show.first_episode is None and show.last_episode is None and \
            show.season is None and not show.finished_show:
        return False

    if show.season is not None and show.first_episode is None and \
            not show.finished_season:
        return False

    if show.finished_season and show.season is None:
        return False

    return True
