from typing import Optional

from aiohttp.web import (
    Application as AIOHTTPApplication,
    View as AIOHTTPView,
    Request as AIOHTTPRequest,
    run_app as aiohttp_run_app
)
from aiohttp_apispec import setup_aiohttp_apispec

from app.store import setup_accessors
from app.store.crm.accessor import CrmAccessor
from app.web.config import Config, setup_config
from app.web.middlewares import setup_middlewares
from app.web.routes import setup_routes


class Application(AIOHTTPApplication):
    config: Optional[Config] = None
    database: dict = {}
    crm_accessor: Optional[CrmAccessor] = CrmAccessor


class Request(AIOHTTPRequest):
    @property
    def app(self) -> "Application":
        return super().app


class View(AIOHTTPView):
    @property
    def request(self) -> Request:
        return super().request


app = Application()


def run_app():
    setup_config(app)
    setup_routes(app)
    setup_aiohttp_apispec(
        app,
        title='Learning',
        url='/docs',
        swagger_path='/redoc',
    )
    setup_middlewares(app)
    setup_accessors(app)
    aiohttp_run_app(app)
