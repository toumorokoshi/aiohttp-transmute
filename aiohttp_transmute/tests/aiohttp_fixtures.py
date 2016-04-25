"""
this is a pattern that works with both the standard unittest pattern,
and a pytest pattern as well.

it relies on
"""
import asyncio

def create_loop():
    loop = asyncio.new_event_loop()


def loop(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)

    yield loop

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
