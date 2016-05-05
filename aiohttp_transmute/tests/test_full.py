import pytest


@pytest.mark.asyncio
async def test_full_app(client_request):
    resp = await client_request('GET', '/')
    assert 200 == resp.status
    text = await resp.text()
    assert "Hello" in text
