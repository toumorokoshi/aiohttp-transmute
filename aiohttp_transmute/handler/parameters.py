from transmute_core.exceptions import APIException


def _get_param_extractor(transmute_func, context):
    if "GET" in transmute_func.http_methods:
        return _get_queryparam_extractor(transmute_func, context)
    else:
        return _get_body_extractor(transmute_func, context)


def _get_queryparam_extractor(transmute_func, context):

    signature = transmute_func.signature
    all_args = set()
    add_request = False
    for arg in signature.args + list(signature.kwargs.values()):
        if arg.name == "request":
            add_request = True
            continue
        all_args.add(arg)

    async def _get_queryparams(request):
        args = {}
        if add_request:
            args["request"] = request
        _add_match_info(request, args)
        for arg in all_args:
            if arg.name in args:
                continue
            if arg.name in request.GET:
                args[arg.name] = context.serializers.load(
                    arg.type, request.GET[arg.name]
                )
                continue

            if arg.default != signature.NoDefault:
                args[args.name] = arg.default
                continue

            raise APIException("required parameter {0} was not passed.".format(arg.name))
        return args

    return _get_queryparams


def _get_body_extractor(transmute_func, context):

    signature = transmute_func.signature
    all_args = set()
    add_request = False
    for arg in signature.args + list(signature.kwargs.values()):
        if arg.name == "request":
            add_request = True
            continue
        all_args.add(arg)

    async def _get_body_params(request):
        args = {}
        content = await request.content.read()
        serializer = context.contenttype_serializers[request.content_type]
        body_dict = serializer.load(content)
        if add_request:
            args["request"] = request
        _add_match_info(request, args)
        for arg in all_args:
            if arg.name in args:
                continue
            if arg.name in body_dict:
                args[arg.name] = context.serializers.load(
                    arg.type, body_dict[arg.name]
                )
                continue

            if arg.default != signature.NoDefault:
                args[args.name] = arg.default

            raise APIException("required parameter {0} was not passed.".format(arg.name))
        return args

    return _get_body_params


def _add_match_info(request, args):
    for k, v in request.match_info.items():
        args[k] = v
