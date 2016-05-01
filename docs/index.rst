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

    # annotating a route
    # adding swagger

    from aiohttp import web
    import aiohttp_transmute

    # define a GET endpoint, taking a query parameter integers left and right,
    # which must be integers.
    @aiohttp_transmute.to_route()
    async def multiply(request, name: str, left: int, right: int) -> int:
        return left + right

    app = web.Application()
    app.router.add_route('GET', '/{name}', multiply)
    # this should be at the end, to ensure all routes are considered when
    # constructing the handler.
    # this will add a swagger.json definition
    aiohttp_transmute.add_swagger(app, "/swagger.json", "/swagger")
    web.run_app(app)


Contents:

.. toctree::
   :maxdepth: 2

   routes
   serialization
   swagger


aiohttp-transmute is a transmute framework for `aiohttp
<http://aiohttp.readthedocs.org/>`_.

Read the users guide



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
