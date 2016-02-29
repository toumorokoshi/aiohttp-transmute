from functools import wraps
from .parameters import _get_param_extractor
from web_transmute import contenttype_serializers, serializers
from aiohttp import web


def create_handler(transmute_func, method=None):
    method = method or next(iter(transmute_func.http_methods))

    extract_params = _get_param_extractor(transmute_func)

    @wraps(transmute_func.raw_func)
    async def handler(request):
        args = await extract_params(request)
        try:
            output = {
                "result": await transmute_func.raw_func(**args),
                "code": 200,
                "success": True
            }
        except Exception as e:
            output = {
                "result": "as exception occurred: ".format(str(e)),
                "success": False
            }
        if transmute_func.return_type:
            output = serializers[transmute_func.return_type].dump(output)
        body = contenttype_serializers.to_type(request.content_type, output)
        return web.Response(
            body=body
        )

    handler.transmute_func = transmute_func
    return handler
