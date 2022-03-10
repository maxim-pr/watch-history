from aiohttp import web

from ..services.watch_history import WatchHistoryService


class BaseHandler(web.View):

    def __init__(self, request: web.Request):
        if request.get('user_id') is None:
            raise web.HTTPUnauthorized()
        super().__init__(request)

    @property
    def user_id(self) -> str:
        return self.request['user_id']

    @property
    def watch_history_service(self) -> WatchHistoryService:
        return self.request.app['services']['watch_history']
