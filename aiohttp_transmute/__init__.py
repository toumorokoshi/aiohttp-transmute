from web_transmute import *
from web_transmute.function import TransmuteFunction
from .handler import create_handler


def to_route(**options):

    def decorator(fn):
        transmute_func = TransmuteFunction(fn, **options)
        return create_handler(transmute_func)

    return decorator
