from functools import wraps
from .parameters import _get_param_extractor
from web_transmute import default_context
from web_transmute.contenttype_serializers import NoSerializerFound
from web_transmute.exceptions import ApiException
from aiohttp import web


def create_handler(transmute_func, method=None, context=default_context):
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
        except ApiException as e:
            output = {
                "result": "invalid api use: {0}".format(str(e)),
                "success": False
            }
        try:
            body = context.contenttype_serializers.to_type(
                request.content_type, output
            )
        except NoSerializerFound:
            body = context.contenttype_serializers.to_type("json", output)
        return web.Response(
            body=body
        )

    handler.transmute_func = transmute_func
    return handler
