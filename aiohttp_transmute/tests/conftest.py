import asyncio
import pytest
import socket
from .example import create_app
from aiohttp import request


@pytest.yield_fixture
def event_loop():
    policy = asyncio.get_event_loop_policy()
    res = policy.new_event_loop()
    _close = res.close
    res.close = lambda: None

    yield res
    _close()


@pytest.fixture
def app(event_loop):
    return create_app(event_loop)


@pytest.yield_fixture
def srv_and_url(app, event_loop):
    srv, url, handler = create_server(app)
    yield srv, url, handler
    teardown_server(app, srv, handler)


@pytest.yield_fixture
def client_request(event_loop, app, srv_and_url):
    srv, root, handler = srv_and_url
    async def func(method, url, *args,  **kwargs):
        """
        a convenience method provided to perform a request
        against the current server.
        """
        url = root + url
        return await request(method, url, *args,
                             loop=event_loop, **kwargs)
    yield func


def create_server(app, proto="http"):
    loop = app.loop
    port = unused_port()
    handler = app.make_handler()
    srv = loop.run_until_complete(loop.create_server(
        handler, '127.0.0.1', port
    ))
    url = "{}://127.0.0.1:{}".format(proto, port)
    return srv, url, handler


def teardown_server(app, srv, handler):
    loop = app.loop
    # kill handler
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.run_until_complete(app.shutdown())
    loop.run_until_complete(handler.finish_connections())
    loop.run_until_complete(app.cleanup())


def unused_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]
