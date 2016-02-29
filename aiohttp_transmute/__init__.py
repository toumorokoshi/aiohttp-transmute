from web_transmute import *
from web_transmute.function import TransmuteFunction
from aiohttp.web import UrlDispatcher
from .handler import create_handler
from swagger_schema import Paths, Path


def to_route(**options):

    def decorator(fn):
        transmute_func = TransmuteFunction(fn, **options)
        return create_handler(transmute_func)

    return decorator


class TransmuteUrlDispatcher(UrlDispatcher):

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
        return self._swagger
