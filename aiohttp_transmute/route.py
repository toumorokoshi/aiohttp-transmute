from collections import OrderedDict
from transmute_core import default_context, describe
from transmute_core.function import TransmuteFunction
from .handler import create_handler
from .swagger import SWAGGER_SCHEMA_KEY


def add_transmute_route(*args, context=default_context):
    """
    two formats are accepted, for transmute routes. One allows
    for a more traditional aiohttp syntax, while the other
    allows for a variant with the route predefined.

    .. code-block:: python

        # if the path and method are not added in describe.
        add_transmute_route(app, "GET", "/route", fn)

        # if the path and method are already added in describe
        add_transmute_route(app, fn)
    """
    if len(args) == 2:
        app, fn = args
    elif len(args) == 4:
        app, methods, paths, fn = args
        describe(methods=methods, paths=paths)(fn)
    else:
        raise ValueError(
            "expected one or three arguments for add_transmute_route!"
        )
    if SWAGGER_SCHEMA_KEY not in app:
        app[SWAGGER_SCHEMA_KEY] = {}
    swagger = app[SWAGGER_SCHEMA_KEY]
    transmute_func = TransmuteFunction(
        fn,
        args_not_from_request=["request"]
    )
    handler = create_handler(transmute_func, context=context)
    swagger_path = transmute_func.get_swagger_path(context)
    for p in transmute_func.paths:
        # add to swagger
        if p not in swagger:
            swagger[p] = swagger_path
        else:
            for method, definition in swagger_path.items():
                setattr(swagger[p], method, definition)

        # add to aiohttp
        aiohttp_path = _convert_to_aiohttp_path(p)
        resource = app.router.add_resource(aiohttp_path)
        for method in transmute_func.methods:
            resource.add_route(method, handler)


def _convert_to_aiohttp_path(path):
    """ convert a transmute path to one supported by aiohttp. """
    return path
