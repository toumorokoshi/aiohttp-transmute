import asyncio
import json
from aiohttp import web
from aiohttp_transmute import (
    to_route, TransmuteUrlDispatcher,
    add_swagger_api_route,
    create_swagger_json_handler
)
from swagger_schema import Swagger, Info

async def handle(request):
    text = "Hello, can you hear me?"
    return web.Response(body=text.encode('utf-8'))


@to_route()
async def multiply(request, left: int, right: int) -> int:
    return left + right


async def init(loop):
    app = web.Application(loop=loop, router=TransmuteUrlDispatcher())
    app.router.add_route('GET', '/', handle)
    app.router.add_route('GET', '/multiply', multiply)
    # this should be at the end, to ensure all routes are considered when
    # constructing the handler.
    app.router.add_route('GET', '/swagger.json',
                         create_swagger_json_handler(app))
    add_swagger_api_route(app, "/swagger", "/swagger.json")
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8080)
    return srv


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

main()
