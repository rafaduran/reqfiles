'''Setuptools setup script.'''
from setuptools import setup

import reqfiles

REQUIRES = {}


setup(d2to1=True, version=reqfiles.__version__, **REQUIRES)
