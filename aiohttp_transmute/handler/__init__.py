from functools import wraps
from .parameters import _get_param_extractor
from web_transmute import contenttype_serializers


def create_handler(transmute_func, method=None):
    method = method or next(iter(transmute_func.http_methods))

    extract_params = _get_param_extractor(transmute_func)

    @wraps(transmute_func.raw_func)
    async def handler(request):
        args = await extract_params(request)
        output = await transmute_func.raw_func(**args)
        return contenttype_serializers.to_type(request.content_type, output)

    return handler
