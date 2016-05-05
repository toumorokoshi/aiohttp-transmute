from .fixtures import AiohttpTestClass
from aiohttp import web


async def handle(request):
    text = "Hello, can you hear me?"
    return web.Response(body=text.encode('utf-8'))


class MyExampleTest(AiohttpTestClass):

    def get_app(self, loop):
        app = web.Application(loop=loop)
        app.router.add_route('GET', '/', handle)
        return app

    def test_hello_world(self):
        result = self.loop.run_until_complete(
            self.request("GET", "/")
        )
        result_text = self.loop.run_until_complete(
            result.text()
        )
        assert "Hello, can you hear me?" in result_text
