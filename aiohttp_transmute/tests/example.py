import asyncio
from aiohttp import web
from aiohttp_transmute import to_route

async def handle(request):
    text = "Hello, can you hear me?"
    return web.Response(body=text.encode('utf-8'))


@to_route()
async def multiply(left: int, right: int) -> int:
    return left + right


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', handle)
    app.router.add_route('GET', '/multiply', multiply)
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
