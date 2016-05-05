=================
Autodocumentation
=================

To allow aiohttp-transmute to autodocument your library,
you must use the TransmuteUrlDispatcher as your application's router:

.. code-block:: python

    from aiohttp import web
    import aiohttp_transmute

    app = web.Application(
        # a custom router is needed to help find the transmute functions.
        router=aiohttp_transmute.TransmuteUrlDispatcher())
    )


Afterwards, transmute can generate the swagger json and append it in the appropriate location:


.. code-block:: python

    aiohttp_transmute.add_swagger(app, "/swagger.json", "/swagger")


-------------
API Reference
-------------


.. automodule:: aiohttp_transmute.swagger
    :members:

.. autoclass:: aiohttp_transmute.TransmuteUrlDispatcher
