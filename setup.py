'''Setuptools setup script.'''
from setuptools import setup

import reqfiles

setup(d2to1=True, version=reqfiles.__version__, **reqfiles.Reqfiles())
