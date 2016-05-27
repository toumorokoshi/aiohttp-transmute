import pytest
import json


# TODO:
@pytest.mark.asyncio
async def test_unsupported_contenttype_sent():
    """ an unsupported contenttype should return a 400 """
    raise Exception()


@pytest.mark.asyncio
async def test_full_app(client_request):
    resp = await client_request('GET', '/')
    assert 200 == resp.status
    text = await resp.text()
    assert "Hello" in text


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
    assert json.loads(text)["paths"]["/multiply"] == {
        "get": {
            "produces": ["application/json", "application/x-yaml"],
            "consumes": ["application/json", "application/x-yaml"],
            "responses": {
                "200": {
                    "schema": {
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
                        "required": ["success", "message"],
                        "properties": {
                            "message": {"type": "string"},
                            "success": {"type": "boolean"}
                        }
                    },
                    "description": "invalid input received"}
            },
            "summary": "",
            "description": ""
        }
    }
