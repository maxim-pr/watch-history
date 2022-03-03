from aiohttp import web

from ..base import BaseHandler
from ...models import WatchHistoryFilmRecord, WatchHistoryShowRecord
from ...services.watch_history import FilmAlreadyWatchedError


class AddFilmRecordHandler(BaseHandler):

    async def post(self) -> web.Response:
        request_data = await self.request.json()
        film = WatchHistoryFilmRecord(
            user_id=self.user_id,
            **request_data
        )

        try:
            watch_history_record_id = await self.watch_history_service.\
                add_film(film)
        except FilmAlreadyWatchedError as e:
            response_data = {
                'error': {
                    'message': 'film was already watched by the user',
                    'id': e.record_id
                }
            }
            return web.json_response(data=response_data,
                                     status=web.HTTPBadRequest.status_code)

        response_data = {
            'data': {
                'id': watch_history_record_id
            }
        }
        return web.json_response(data=response_data,
                                 status=web.HTTPCreated.status_code)


class AddShowRecordHandler(BaseHandler):

    async def post(self) -> web.Response:
        request_data = await self.request.json()
        show = WatchHistoryShowRecord(
            user_id=self.user_id,
            **request_data
        )

        watch_history_record_id = await self.watch_history_service.\
            add_show(show)

        response_data = {
            'data': {
                'id': watch_history_record_id
            }
        }
        return web.json_response(data=response_data,
                                 status=web.HTTPCreated.status_code)
