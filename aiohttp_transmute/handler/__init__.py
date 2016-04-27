from functools import wraps
from .parameters import _get_param_extractor
from transmute_core import APIException, NoSerializerFound
from aiohttp import web


def create_handler(transmute_func, context, method=None):
    method = method or next(iter(transmute_func.http_methods))

    extract_params = _get_param_extractor(transmute_func, context)

    @wraps(transmute_func.raw_func)
    async def handler(request):
        args = await extract_params(request)
        try:
            result = await transmute_func.raw_func(**args)
            if transmute_func.return_type:
                result = context.serializers.dump(
                    transmute_func.return_type, result
                )
            output = {
                "result": result,
                "code": 200,
                "success": True
            }
        except APIException as e:
            output = {
                "result": "invalid api use: {0}".format(str(e)),
                "success": False,
                "code": e.code
            }
        try:
            serializer = context.contenttype_serializers[request.content_type]
        except NoSerializerFound:
            serializer = context.contenttype_serializers["json"]
        body = serializer.dump(output)
        return web.Response(
            body=body, status=output["code"]
        )

    handler.transmute_func = transmute_func
    return handler
