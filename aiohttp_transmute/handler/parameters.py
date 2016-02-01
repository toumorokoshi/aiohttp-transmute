from web_transmute.exceptions import ApiException
from web_transmute import serializers, contenttype_serializers


def _get_param_extractor(transmute_func):
    if "GET" in transmute_func.http_methods:
        return _get_queryparam_extractor(transmute_func)
    else:
        return _get_body_extractor(transmute_func)


def _get_queryparam_extractor(transmute_func):

    signature = transmute_func.signature
    all_args = signature.args + list(signature.kwargs.values())

    async def _get_queryparams(request):
        args = {}
        for arg in all_args:
            if arg.name in request.GET:
                args[arg.name] = serializers[arg.type].load(request.GET[arg.name])
                continue

            if arg.default != signature.NoDefault:
                args[args.name] = arg.default
                continue

            raise ApiException("required parameter {0} was not passed.".format(arg.name))
        return args

    return _get_queryparams


def _get_body_extractor(transmute_func):

    signature = transmute_func.signature
    all_args = signature.args + signature.kwargs.values()

    async def _get_body_params(request):
        args = {}
        content = await request.content
        body_dict = contenttype_serializers.from_type(request.content_type, content)
        for arg in all_args:
            if arg.name is body_dict:
                args[arg.name] = serializers[arg.type].load(request.GET[arg.name])
                continue

            if arg.default != signature.NoDefault:
                args[args.name] = arg.default

            raise ApiException("required parameter {0} was not passed.".format(arg.name))
        return args

    return _get_body_params
