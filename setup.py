#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

base = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(base, "README.rst")

is_release = False
if "--release" in sys.argv:
    is_release = True
    sys.argv.remove("--release")

install_requires = [
    'transmute-core>=0.2.11',
    'aiohttp>=1.1.3'
]

tests_require = []

setup(name='aiohttp-transmute',
      setup_requires=["vcver"],
      vcver={
          "is_release": is_release,
          "path": base
      },
      description='a Toolset to generate routes from objects for aiohttp.',
      long_description=open(README_PATH).read(),
      author='Yusuke Tsutsumi',
      author_email='yusuke@tsutsumi.io',
      url='',
      packages=find_packages(),
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
      ],
      tests_require=tests_require
)
