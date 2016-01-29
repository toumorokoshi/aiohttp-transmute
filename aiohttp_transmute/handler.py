from functools import wraps


def create_handler(transmute_func, method=None):
    method = method or next(iter(transmute_func.http_methods[0]))

    param_extractor = _get_param_extractor(transmute_func)

    @wraps(transmute_func.raw_func)
    async def handler(request):
        args = _get_args(transmute_func, request)
        pass


def _get_param_extractor(transmute_func):
    if "GET" in transmute_func.http_methods:
        return _get_queryparam_extractor(transmute_func)
    else:
        return _get_body_extractor(transmute_func)


def _get_queryparam_extractor(transmute_func):

    def _get_queryparams(request):
        pass
