import pytest


@pytest.mark.asyncio
async def test_parsing_multiiple_query_params(client_request):
    resp = await client_request('GET', '/multiple_query_params?tag=foo&tag=bar')
    ret_value = await resp.json()
    assert 200 == resp.status
    assert ret_value["result"] == "foo,bar"


@pytest.mark.asyncio
async def test_parsing_multiiple_query_params_single_tag(client_request):
    resp = await client_request('GET', '/multiple_query_params?tag=foo')
    ret_value = await resp.json()
    assert 200 == resp.status
    assert ret_value["result"] == "foo"
