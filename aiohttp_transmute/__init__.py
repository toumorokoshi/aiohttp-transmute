from transmute_core import *
from transmute_core.function import TransmuteFunction
from transmute_core import default_context
from aiohttp.web import UrlDispatcher
from .handler import create_handler
from .swagger import add_swagger_api_route, create_swagger_json_handler, add_swagger
from swagger_schema import Paths, Path


def to_route(context=default_context, **options):
    """
    convert a function to an aiohttp route

    context: a TransmuteContext object.
    """

    def decorator(fn):
        transmute_func = TransmuteFunction(fn, **options)
        return create_handler(transmute_func, context=context)

    return decorator


class TransmuteUrlDispatcher(UrlDispatcher):
    """
    A UrlDispatcher which instruments the add_route function to
    collect swagger spec data from transmuted functions.
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._swagger = Paths()

    def add_route(self, method, path, handler, *args, name=None, expect_handler=None):
        super().add_route(method, path, handler, *args, name=name, expect_handler=expect_handler)
        transmute_func = getattr(handler, "transmute_func", None)
        if transmute_func:
            if path not in self._swagger:
                self._swagger[path] = Path()
            setattr(self._swagger[path], method.lower(), transmute_func.swagger)

    def swagger_paths(self):
        """
        returns a swagger Paths object representing all transmute
        functions registered.
        """
        return self._swagger
