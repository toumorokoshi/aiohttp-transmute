import asyncio
import gc
import unittest
from .common import (
    create_server, teardown_server,
)
from aiohttp import request


class AiohttpTestClass(unittest.TestCase):

    def get_app(self, loop):
        """
        this method should be overriden
        to return the application object.

        .. code-block:: python
            return web.Application()
        """

    def setUp(self):
        self.loop = self._setup_loop()
        self.app = self.get_app(self.loop)
        self.srv, self.url = create_server(self.app)

    def tearDown(self):
        teardown_server(self.app, self.srv)
        self._teardown_loop(self.loop)

    async def request(self, method, url, *args,  **kwargs):
        """
        a convenience method provided to perform a request
        against the current server.
        """
        url = self.url + url
        return await request(method, url, *args,
                             loop=self.loop, **kwargs)

    @classmethod
    def _setup_loop(cls):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        return loop

    @classmethod
    def _teardown_loop(cls, loop):
        is_closed = getattr(loop, 'is_closed')
        if is_closed is not None:
            closed = is_closed()
        else:
            closed = loop._closed
        if not closed:
            loop.call_soon(loop.stop)
            loop.run_forever()
            loop.close()
        gc.collect()
        asyncio.set_event_loop(None)
