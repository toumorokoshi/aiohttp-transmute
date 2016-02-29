import asyncio
import json
from aiohttp import web
from aiohttp_transmute import to_route, TransmuteUrlDispatcher
from swagger_schema import Swagger, Info

async def handle(request):
    text = "Hello, can you hear me?"
    return web.Response(body=text.encode('utf-8'))


@to_route()
async def multiply(request, left: int, right: int) -> int:
    return left + right


_spec = None

async def swagger(request):
    global _spec
    if _spec is None:
        _spec = Swagger(
            info=Info(title="example", version="1.0"),
            paths=request.app.router.swagger_paths(),
            swagger="2.0",
        ).dump()

    return web.Response(
        # we allow CORS, so this can be requested at swagger.io
        headers={
            "Access-Control-Allow-Origin": "*"
        },
        body=json.dumps(_spec).encode('utf-8')
    )


async def init(loop):
    app = web.Application(loop=loop, router=TransmuteUrlDispatcher())
    app.router.add_route('GET', '/', handle)
    app.router.add_route('GET', '/multiply', multiply)
    app.router.add_route('GET', '/swagger', swagger)
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
