import pytest
import json


# TODO:
@pytest.mark.asyncio
async def _test_unsupported_contenttype_sent():
    """ an unsupported contenttype should return a 400 """
    raise Exception()


@pytest.mark.asyncio
async def test_content_type_in_response(client_request):
    """ the content type should be specified in the response. """
    resp = await client_request('GET', '/optional')
    assert 200 == resp.status
    assert resp.headers['Content-Type'] == 'application/json'


@pytest.mark.asyncio
async def test_multiply(client_request):
    resp = await client_request('GET', '/multiply?left=5&right=10')
    assert 200 == resp.status
    text = await resp.text()
    assert json.loads(text) == {
        "result": 50,
        "success": True,
        "code": 200
    }


@pytest.mark.asyncio
async def test_multiply_bad_int(client_request):
    resp = await client_request('GET', '/multiply?left=foo&right=0x00')
    assert 400 == resp.status
    ret_value = await resp.json()
    assert ret_value["success"] is False
    assert ret_value["code"] == 400


@pytest.mark.asyncio
async def test_optional(client_request):
    resp = await client_request('GET', '/optional')
    assert 200 == resp.status
    ret_value = await resp.json()
    assert ret_value["result"] is False


@pytest.mark.asyncio
async def test_optional_with_value(client_request):
    resp = await client_request('GET', '/optional?include_foo=true')
    assert 200 == resp.status
    ret_value = await resp.json()
    assert ret_value["result"] is True


@pytest.mark.asyncio
async def test_describe_later(client_request):
    resp = await client_request('GET', '/describe_later')
    assert 200 == resp.status
    ret_value = await resp.json()
    assert ret_value["success"] is True
    assert ret_value["result"] == "foo"


@pytest.mark.asyncio
async def test_get_id(client_request):
    resp = await client_request('GET', '/id/10')
    assert 200 == resp.status
    text = await resp.text()
    assert json.loads(text) == {
        "result": "your id is: 10",
        "success": True,
        "code": 200
    }


@pytest.mark.asyncio
async def test_config(client_request):
    resp = await client_request('GET', '/config')
    assert 200 == resp.status
    text = await resp.text()
    assert json.loads(text) == {
        "result": {"test": "foo"},
        "success": True,
        "code": 200
    }


@pytest.mark.asyncio
async def test_swagger(client_request):
    resp = await client_request('GET', '/swagger.json')
    assert 200 == resp.status
    text = await resp.text()
    assert json.loads(text)["paths"]["/multiply"]["get"]["responses"] == {
        "200": {
            "schema": {
                "title": "SuccessObject",
                "required": ["success", "result"],
                "properties": {
                    "result": {"type": "number"},
                    "success": {"type": "boolean"}
                }
            },
            "description": "success"
        },
        "400": {
            "schema": {
                "title": "FailureObject",
                "required": ["success", "message"],
                "properties": {
                    "message": {"type": "string"},
                    "success": {"type": "boolean"}
                }
            },
            "description": "invalid input received"}
    }
