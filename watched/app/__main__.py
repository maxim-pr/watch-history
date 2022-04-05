import gunicorn.app.base
from aiohttp import web
from configargparse import Namespace

from .app import create_app
from .config import parse_args


class WebServer(gunicorn.app.base.BaseApplication):
    def __init__(self, args: Namespace, options=None):
        self.args = args
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> web.Application:
        return create_app(self.args)


def main():
    args = parse_args()
    options = {
        'bind': f'{args.api_host}:{str(args.api_port)}',
        'worker_class': 'aiohttp.GunicornWebWorker',
        'workers': 4
    }
    WebServer(args, options).run()


if __name__ == '__main__':
    main()
