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

-----------------
API Documentation
-----------------

.. autofunction:: aiohttp_transmute.to_route
