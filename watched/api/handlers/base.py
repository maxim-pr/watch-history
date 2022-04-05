from aiohttp import web

from ..service import Service


class BaseHandler(web.View):
    def __init__(self, request: web.Request):
        super().__init__(request)

    @property
    def user_id(self) -> str:
        return self.request.headers['User-ID']

    @property
    def service(self) -> Service:
        return self.request.app['service']
