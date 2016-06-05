from aiohttp.web import UrlDispatcher
from transmute_core import default_context
from transmute_core.function import TransmuteFunction
from .handler import create_handler


class TransmuteUrlDispatcher(UrlDispatcher):
    """
    A UrlDispatcher which instruments the add_route function to
    collect swagger spec data from transmuted functions.
    """

    def __init__(self, *args, context=default_context, **kwargs):
        super().__init__()
        self._transmute_context = context
        self._swagger = {}

    def add_transmute_route(self, fn):
        transmute_func = TransmuteFunction(fn, args_not_from_request=["request"])
        handler = create_handler(
            transmute_func, context=self._transmute_context
        )
        swagger_path = transmute_func.get_swagger_path(self._transmute_context)
        for p in transmute_func.paths:
            # add to swagger
            if p not in self._swagger:
                self._swagger[p] = swagger_path
            else:
                for method, definition in swagger_path.items():
                    setattr(self._swagger[p], method, definition)

            # add to aiohttp
            aiohttp_path = self._convert_to_aiohttp_path(p)
            resource = self.add_resource(aiohttp_path)
            for method in transmute_func.methods:
                resource.add_route(method, handler)

    def swagger_paths(self):
        """
        returns a swagger Paths object representing all transmute
        functions registered.
        """
        return self._swagger

    @staticmethod
    def _convert_to_aiohttp_path(path):
        """ convert a transmute path to one supported by aiohttp. """
        return path
