import pytest
from .fixtures.common import (
    create_server, teardown_server
)
from .example import create_app
from aiohttp import request


@pytest.fixture
def app(event_loop):
    return create_app(event_loop)


@pytest.yield_fixture
def srv_and_url(app):
    srv, url = create_server(app)
    yield srv, url
    teardown_server(app, srv)


@pytest.fixture
def client_request(event_loop, srv_and_url):
    srv, root = srv_and_url
    async def func(method, url, *args,  **kwargs):
        """
        a convenience method provided to perform a request
        against the current server.
        """
        url = root + url
        return await request(method, url, *args,
                             loop=event_loop, **kwargs)
    return func
