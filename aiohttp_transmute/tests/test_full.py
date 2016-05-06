import pytest
import json


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
async def test_swagger(client_request):
    resp = await client_request('GET', '/swagger.json')
    assert 200 == resp.status
    text = await resp.text()
    assert json.loads(text) == {
        "swagger": "2.0",
        "paths": {
            "/multiply": {
                "get": {
                    "produces": ["application/json"],
                    "consumes": ["application/json"],
                    "responses": {
                        "200": {
                            "schema": {
                                "required": ["success", "result"],
                                "properties": {
                                    "result": {"type": "string"},
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
                    "description": ""}
            }
        },
        "info": {"title": "example", "version": "1.0"}
    }
