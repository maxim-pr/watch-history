from aiohttp import web

from ..service import Service


class BaseView(web.View):

    @property
    def service(self) -> Service:
        return self.request.app['service']
