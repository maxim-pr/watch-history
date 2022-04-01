# from aiohttp import web
#
# from .base import BaseHandler
# from watched.models import TypeFilter, StatusFilter
#
#
# class GetWatchHistoryHandler(BaseHandler):
#
#     async def get(self) -> web.Response:
#         try:
#             type_filter, status_filter = self._retrieve_filters()
#         except ValueError:
#             response_data = {
#                 'error': {
#                     'message': 'invalid filters'
#                 }
#             }
#             return web.json_response(data=response_data,
#                                      status=web.HTTPBadRequest.status_code)
#
#         watch_history = await self.service.get_watch_history(
#             self.user_id, type_filter, status_filter
#         )
#
#         response_text = ('{', f'"data": {watch_history.json()}', '}')
#         return web.json_response(text=''.join(response_text),
#                                  status=web.HTTPOk.status_code)
#
#     def _retrieve_filters(self) -> tuple[TypeFilter,
#                                          StatusFilter]:
#         """
#         :raises ValueError:
#         """
#         type_filter = TypeFilter.ALL
#         status_filter = StatusFilter.ALL
#
#         if self.request.query.get('type') is not None:
#             type_filter = TypeFilter(
#                 self.request.query['type']
#             )
#         if self.request.query.get('status'):
#             status_filter = StatusFilter(
#                 self.request.query['status']
#             )
#
#         return type_filter, status_filter
