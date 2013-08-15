'''Setuptools setup script.'''
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

import reqfiles

README = open('README.rst', 'rt').read()

setup(name='reqfiles',
      version=reqfiles.__version__,
      author='Rafael Durán Castañeda',
      author_email='rafadurancastaneda@gmail.com',
      description=README,
      license='BSD',
      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
      ],
      keywords='Pip Requirements Setuptools Distutils',
      packages=find_packages(exclude=('tests',)),
      entry_points={
          'distutils.setup_keywords': [
              'reqfiles = reqfiles.setuptools:reqfiles'
          ]
      },
      **reqfiles.Reqfiles())
