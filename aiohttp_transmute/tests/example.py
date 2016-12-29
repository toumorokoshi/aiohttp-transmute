from aiohttp import web
import aiohttp_transmute
from aiohttp_transmute import (
    describe, add_swagger, add_route, route
)
from aiohttp.errors import HttpProcessingError

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


@aiohttp_transmute.describe(paths="/aiohttp_error")
async def error(request):
    raise HttpProcessingError(code=403, message="unauthorized")


@aiohttp_transmute.describe(
    paths="/body_and_header",
    methods="POST",
    body_parameters=["body"],
    header_parameters=["header"]
)
async def body_and_header(request, body: str, header: str) -> bool:
    return body == header


@aiohttp_transmute.describe(paths="/config")
async def config(request):
    return request.app["config"]


@aiohttp_transmute.describe(paths="/multiple_query_params")
async def multiple_query_params(tag: [str]) -> str:
    return ",".join(tag)


def create_app(loop):
    app = web.Application(loop=loop)
    app["config"] = {"test": "foo"}
    app.router.add_route('GET', '/', handle)
    add_route(app, multiple_query_params)
    add_route(app, multiply)
    add_route(app, get_id)
    route(app, config)
    route(app, get_optional)
    route(app, body_and_header)
    route(app, error)
    # this should be at the end, to ensure all routes are considered when
    # constructing the handler.
    add_swagger(app, "/swagger.json", "/swagger")
    return app
