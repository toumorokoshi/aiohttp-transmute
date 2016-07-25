from aiohttp import web
import aiohttp_transmute
from aiohttp_transmute import (
    describe, TransmuteUrlDispatcher, add_swagger
)

async def handle(request):
    text = "Hello, can you hear me?"
    return web.Response(body=text.encode('utf-8'))


@aiohttp_transmute.describe(paths="/multiply")
async def multiply(request, left: int, right: int) -> int:
    return left * right


@aiohttp_transmute.describe(paths="/id/{my_id}")
async def get_id(request, my_id: str) -> str:
    return "your id is: " + my_id


@aiohttp_transmute.describe(paths="/optional")
async def get_optional(request, include_foo: bool=False) -> bool:
    return include_foo


@aiohttp_transmute.describe(paths="/config")
async def config(request):
    return request.app["config"]


@aiohttp_transmute.describe()
async def describe_later() -> str:
    return "foo"


async def multiple_query_params(tag: [str]) -> str:
    return ",".join(tag)


def create_app(loop):
    app = web.Application(loop=loop, router=TransmuteUrlDispatcher())
    app["config"] = {"test": "foo"}
    app.router.add_route('GET', '/', handle)
    # the preferred form.
    app.router.add_transmute_route("GET", "/describe_later", describe_later)
    app.router.add_transmute_route("GET", "/multiple_query_params", multiple_query_params)
    # the legacy form should be supported.
    app.router.add_transmute_route(multiply)
    app.router.add_transmute_route(get_id)
    app.router.add_transmute_route(config)
    app.router.add_transmute_route(get_optional)
    # this should be at the end, to ensure all routes are considered when
    # constructing the handler.
    add_swagger(app, "/swagger.json", "/swagger")
    return app
