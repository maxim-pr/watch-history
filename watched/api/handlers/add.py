from aiohttp import web

from .base import BaseHandler
from ..dto import AddFilmRecordDTO, AddShowRecordDTO
from ..errors import FilmAlreadyWatched, ShowRecordInconsistency


class AddFilmRecordHandler(BaseHandler):
    async def post(self) -> tuple[int, dict]:
        request_data = await self.request.json()
        dto = AddFilmRecordDTO(user_id=self.user_id, **request_data)

        try:
            record_id = await self.service.add_film_record(dto)
        except FilmAlreadyWatched as e:
            data = {
                'message': 'film was already watched by the user',
                'id': e.record_id
            }
            return web.HTTPBadRequest.status_code, data

        data = {'id': record_id}
        return web.HTTPCreated.status_code, data


class AddShowRecordHandler(BaseHandler):
    async def post(self) -> tuple[int, dict]:
        request_data = await self.request.json()
        dto = AddShowRecordDTO(user_id=self.user_id, **request_data)

        try:
            record_id, media_id = await self.service.add_show_record(dto)
        except ShowRecordInconsistency as e:
            data = {
                'message': 'inconsistent show record',
                'prev_show_record': e.prev_record.dict()
            }
            return web.HTTPBadRequest.status_code, data

        data = {'id': record_id}
        if dto.media_id is None:
            data['media_id'] = media_id
        return web.HTTPCreated.status_code, data
