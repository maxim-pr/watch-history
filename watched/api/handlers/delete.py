# from aiohttp import web
#
# from watched.api.handlers.base import BaseHandler
#
#
# class DeleteRecordHandler(BaseHandler):
#
#     async def delete(self) -> web.Response:
#         record_id = self.request.match_info['id']
#
#         await self.service.delete_record(record_id)
#
#         return web.Response(status=web.HTTPNoContent.status_code)
