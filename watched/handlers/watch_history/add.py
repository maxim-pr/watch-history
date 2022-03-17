from aiohttp import web

from ..base import BaseHandler
from ...models import WatchHistoryFilmRecord, WatchHistoryShowRecord
from ...services.watch_history import FilmAlreadyWatched, \
    InconsistentShowRecord


class AddFilmRecordHandler(BaseHandler):

    async def post(self) -> web.Response:
        request_data = await self.request.json()
        film_record = WatchHistoryFilmRecord(
            user_id=self.user_id,
            **request_data
        )

        try:
            record_id = await self.watch_history_service.add_film_record(film_record)
        except FilmAlreadyWatched as e:
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
                'id': record_id
            }
        }
        return web.json_response(data=response_data,
                                 status=web.HTTPCreated.status_code)


class AddShowRecordHandler(BaseHandler):

    async def post(self) -> web.Response:
        request_data = await self.request.json()
        show_record = WatchHistoryShowRecord(
            user_id=self.user_id,
            **request_data
        )
        if show_record.show_id is None and show_record.show_name is None:
            return web.HTTPBadRequest()
        if show_record.show_id is not None and show_record.show_name is not None:
            return web.HTTPBadRequest()

        try:
            record_id = await self.watch_history_service.\
                add_show_record(show_record)
        except InconsistentShowRecord as e:
            response_data = {
                'error': {
                    'message': 'inconsistent show record',
                    'last_show_record': e.last_show_record.json()
                }
            }
            return web.json_response(data=response_data,
                                     status=web.HTTPBadRequest.status_code)

        response_data = {
            'data': {
                'id': record_id
            }
        }
        return web.json_response(data=response_data,
                                 status=web.HTTPCreated.status_code)
