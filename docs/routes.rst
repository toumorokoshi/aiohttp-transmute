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
    @aiohttp_transmute.to_route()
    async def multiply(request, name: str, left: int, right: int) -> int:
        return left + right

    # append to your route later
    app.router.add_route('GET', '/{name}', multiply)

------------------------
query parameters vs body
------------------------

As with most transmute frameworks, a GET transmute function
will use queryparamters as the function arguments, while every
other request type will assume the body is a dictionary, and
parse the body.

.. code-block:: python

    import aiohttp_transmute

    @aiohttp_transmute.to_route()
    # interpreted as query parameters
    async def multiply(request, name: str, left: int, right: int) -> int:
        return left + right

    # interpreted as body parameters
    @aiohttp_transmute.to_route()
    @aiohttp_transmute.POST
    async def multiply_post(request, name: str, left: int, right: int) -> int:
        return left + right

    # append to your route later
    app.router.add_route('GET', '/{name}', multiply)
    app.router.add_route('POST', '/{name}', multiply_post)

-----------------
API Documentation
-----------------

.. autofunction:: aiohttp_transmute.to_route
