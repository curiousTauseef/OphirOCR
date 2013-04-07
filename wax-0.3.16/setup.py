#!/usr/bin/env python

from distutils.core import setup
import wax

setup(name='wax',
      version=wax.WAX_VERSION,
      description='Wax wxPython wrapper',
      author='Hans Nowak',
      author_email='hans@zephyrfalcon.org',
      url='http://zephyrfalcon.org/labs/wax.html',
      packages=['wax'],
      package_data={'wax': ['*.txt']},
)
