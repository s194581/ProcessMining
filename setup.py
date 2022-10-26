# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simplest setup.py
"""
import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'cc-dcr'
DESCRIPTION = 'My short description for my project.'
URL = 'https://gitlab.cs.fau.de/is/projects/cc-dcr'
EMAIL = 'sebastian.dunzer@fau.de'
AUTHOR = 'Sebastian Dunzer'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = 1.0

# What packages are required for this module to be executed?
REQUIRED = [
    'pandas', 'opyenxes', 'sphinx', 'twine'
]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/reStructuredText',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',

)
