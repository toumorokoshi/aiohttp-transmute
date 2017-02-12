=========
Changelog
=========

------------------------------
Backwards incompatible changes
------------------------------

0.6.0
=====

To be released March 1st, 2017. TransmuteUrlDispatcher will be removed.

0.5.0
=====

The legacy pattern of TransmuteUrlDispatcher now requires manual execution of
post_init, due to a change in aiohttp (https://github.com/KeepSafe/aiohttp/issues/1373) :

.. code:: python

    router = TransmuteUrlDispatcher()
    app = web.Application(
        loop=loop,
        router=router
        middlewares=[db_connection_factory]
    )
    router.post_init(app)
