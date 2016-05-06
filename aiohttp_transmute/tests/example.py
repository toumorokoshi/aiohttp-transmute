from aiohttp import web
from aiohttp_transmute import (
    to_route, TransmuteUrlDispatcher,
    add_swagger_api_route,
    create_swagger_json_handler
)

async def handle(request):
    text = "Hello, can you hear me?"
    return web.Response(body=text.encode('utf-8'))


@to_route()
async def multiply(request, left: int, right: int) -> int:
    return left * right


def create_app(loop):
    app = web.Application(loop=loop, router=TransmuteUrlDispatcher())
    app.router.add_route('GET', '/', handle)
    app.router.add_route('GET', '/multiply', multiply)
    # this should be at the end, to ensure all routes are considered when
    # constructing the handler.
    app.router.add_route('GET', '/swagger.json',
                         create_swagger_json_handler(app))
    add_swagger_api_route(app, "/swagger", "/swagger.json")
    return app
