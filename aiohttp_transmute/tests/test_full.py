import pytest


async def handle(request):
    text = "Hello, can you hear me?"
    return web.Response(body=text.encode('utf-8'))


@pytest.mark.run_loop
def test_full_app(create_app_and_client):
    app, client = await create_app_and_client()
    app.router.add_route('GET', '/', handle)
    resp = await client.get('/')
    assert 200 = resp.status
    text = await resp.text()
    assert "Hello" in resp.text()
