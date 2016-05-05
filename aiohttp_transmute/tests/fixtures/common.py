"""
this is a pattern that works with both the standard unittest pattern,
and a pytest pattern as well.

for pytest, the fixtures from pytest-asyncio are used.

for unittest, there is a standard setup/teardown pattern
"""
import socket


def create_server(app, proto="http"):
    loop = app.loop
    port = unused_port()
    handler = app.make_handler()
    srv = loop.run_until_complete(loop.create_server(
        handler, '127.0.0.1', port
    ))
    url = "{}://127.0.0.1:{}".format(proto, port)
    return srv, url


def teardown_server(app, srv):
    loop = app.loop
    # kill handler
    loop.run_until_complete(app.finish())
    srv.close()
    loop.run_until_complete(srv.wait_closed())


def unused_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]
