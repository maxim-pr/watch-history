import logging
from typing import Optional

from aiohttp import web

from .base import BaseHandler
from ..dto import UpdateFilmRecordDTO
from ..errors import RecordDoesNotExist, AccessError, MediaTypeInconsistency

logger = logging.getLogger(__name__)


class UpdateFilmRecordHandler(BaseHandler):

    async def put(self) -> tuple[int, Optional[dict]]:
        record_id = self.request.match_info['id']
        request_data = await self.request.json()
        dto = UpdateFilmRecordDTO(record_id=record_id, user_id=self.user_id,
                                  **request_data)

        try:
            await self.service.update_film_record(dto)
        except RecordDoesNotExist:
            return web.HTTPNotFound.status_code, None
        except AccessError as e:
            logger.exception(e, exc_info=True)
            return web.HTTPForbidden.status_code, None
        except MediaTypeInconsistency:
            response_data = {
                'error': {
                    'message': 'provided record_id corresponds to show record'
                }
            }
            return web.HTTPBadRequest.status_code, response_data

        return web.HTTPNoContent.status_code, None
