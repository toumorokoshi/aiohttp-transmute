.. aiohttp-transmute documentation master file, created by
   sphinx-quickstart on Mon May  9 23:13:22 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

aiohttp-transmute
=================

A transmute framework for `aiohttp <http://aiohttp.readthedocs.org/>`_. This framework
provides:

* declarative generation of http handler interfaces by parsing function annotations
* validation and serialization to and from a variety of content types (e.g. json or yaml).
* validation and serialization to and from native python objects, using `schematics <http://schematics.readthedocs.org/en/latest/>`_.
* autodocumentation of all handlers generated this way, via `swagger <http://swagger.io/>`_.

-------
Example
-------

.. code-block:: python

    from aiohttp import web
    import aiohttp_transmute

    # define a GET endpoint, taking a query parameter integers left and right,
    # which must be integers.
    @aiohttp_transmute.to_route()
    async def multiply(request, name: str, left: int, right: int) -> int:
        return left + right

    app = web.Application(
        # a custom router is needed to help find the transmute functions.
        router=aiohttp_transmute.TransmuteUrlDispatcher())
    )
    app.router.add_route('GET', '/{name}', multiply)
    # this should be at the end, to ensure all routes are considered when
    # constructing the handler.
    # this will add:
    #   - a swagger.json definition
    #   - a static page that renders the swagger.json
    aiohttp_transmute.add_swagger(app, "/swagger.json", "/swagger")
    web.run_app(app)


Contents:

.. toctree::
   :maxdepth: 2

   routes
   serialization
   documentation
