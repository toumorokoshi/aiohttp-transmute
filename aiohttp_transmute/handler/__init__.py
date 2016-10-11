from functools import wraps
from .parameters import extract_params
from transmute_core import APIException, NoSerializerFound
from aiohttp import web


def create_handler(transmute_func, context):

    @wraps(transmute_func.raw_func)
    async def handler(request):
        try:
            args, kwargs = await extract_params(request, context,
                                                transmute_func.signature,
                                                transmute_func.parameters)
            result = await transmute_func.raw_func(*args, **kwargs)
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
        content_type = request.content_type
        try:
            serializer = context.contenttype_serializers[content_type]
        except NoSerializerFound:
            serializer = context.contenttype_serializers.default
            content_type = serializer.main_type
        body = serializer.dump(output)
        return web.Response(
            body=body, status=output["code"],
            content_type=content_type
        )

    handler.transmute_func = transmute_func
    return handler
