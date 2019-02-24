.. aiohttp-transmute documentation master file, created by
   sphinx-quickstart on Mon May  9 23:13:22 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

aiohttp-transmute
=================

A `transmute
<http://transmute-core.readthedocs.io/en/latest/index.html>`_
framework for `aiohttp <http://aiohttp.readthedocs.org/>`_. This
framework provides:

* declarative generation of http handler interfaces by parsing function annotations
* validation and serialization to and from a variety of content types (e.g. json or yaml).
* validation and serialization to and from native python objects, using `schematics <http://schematics.readthedocs.org/en/latest/>`_.
* autodocumentation of all handlers generated this way, via `swagger <http://swagger.io/>`_.

As of February 2019, this library is deprecated in favor of using transmute-core directly. See https://transmute-core.readthedocs.io/en/latest/