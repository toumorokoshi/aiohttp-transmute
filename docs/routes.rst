======
Routes
======

-------
Example
-------

Adding routes follows the standard transmute pattern, with
a decorator converting a function to an aiohttp route:


.. code-block:: python

    import aiohttp_transmute

    # define a GET endpoint, taking a query parameter integers left and right,
    # which must be integers.
    @aiohttp_transmute.describe(paths="/{name}")
    async def multiply(request, name: str, left: int, right: int) -> int:
        return left + right

    # append to your route later
    app.router.add_transmute_route(multiply)

------------------------
query parameters vs body
------------------------

As with most transmute frameworks, a GET transmute function
will use queryparamters as the function arguments, while every
other request type will assume the body is a dictionary, and
parse the body.

.. code-block:: python

    import aiohttp_transmute

    # interpreted as query parameters
    @aiohttp_transmute.describe(paths="/{name}")
    async def multiply(request, name: str, left: int, right: int) -> int:
        return left + right

    # interpreted as body parameters
    @aiohttp_transmute.describe(methods=["POST"], paths="/{name}")
    async def multiply_post(request, name: str, left: int, right: int) -> int:
        return left + right

    # append to your route later
    app.router.add_transmute_route(multiply)
    app.router.add_transmute_route(multiply_post)

-----------------
API Documentation
-----------------

.. autofunction:: aiohttp_transmute.describe
