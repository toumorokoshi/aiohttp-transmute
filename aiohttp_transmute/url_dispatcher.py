from aiohttp.web import UrlDispatcher
from collections import OrderedDict
from transmute_core import default_context, describe
from transmute_core.function import TransmuteFunction
from transmute_core.swagger import SwaggerSpec
from .handler import create_handler


class TransmuteUrlDispatcher(UrlDispatcher):
    """
    A UrlDispatcher which instruments the add_route function to
    collect swagger spec data from transmuted functions.
    """

    def __init__(self, *args, context=default_context, **kwargs):
        super().__init__(app=None)
        self._transmute_context = context
        self._swagger = SwaggerSpec()

    def add_transmute_route(self, *args):
        """
        two formats are accepted, for transmute routes. One allows
        for a more traditional aiohttp syntax, while the other
        allows for a flask-like variant.

        .. code-block:: python

            # if the path and method are not added in describe.
            add_transmute_route("GET", "/route", fn)

            # if the path and method are already added in describe
            add_transmute_route(fn)
        """
        if len(args) == 1:
            fn = args[0]
        elif len(args) == 3:
            methods, paths, fn = args
            describe(methods=methods, paths=paths)(fn)
        else:
            raise ValueError(
                "expected one or three arguments for add_transmute_route!"
            )
        transmute_func = TransmuteFunction(
            fn,
            args_not_from_request=["request"]
        )
        handler = create_handler(
            transmute_func, context=self._transmute_context
        )
        self._swagger.add_func(transmute_func, self._transmute_context)
        swagger_path = transmute_func.get_swagger_path(self._transmute_context)

        for p in transmute_func.paths:
            aiohttp_path = self._convert_to_aiohttp_path(p)
            resource = self.add_resource(aiohttp_path)
            for method in transmute_func.methods:
                resource.add_route(method, handler)

    @property
    def swagger(self):
        """
        returns a swagger Paths object representing all transmute
        functions registered.
        """
        return self._swagger

    @staticmethod
    def _convert_to_aiohttp_path(path):
        """ convert a transmute path to one supported by aiohttp. """
        return path
