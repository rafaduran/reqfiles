'''Setuptools setup script.'''
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

import reqfiles

README = open('README.rst', 'rt').read()

setup(name='reqfiles',
      version=reqfiles.__version__,
      author='Rafael Durán Castañeda',
      author_email='rafadurancastaneda@gmail.com',
      url='https://github.com/rafaduran/reqfiles',
      description='Requirement files Setuptools integration',
      long_description=README,
      license='BSD',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Framework :: Setuptools Plugin',
          'Topic :: System :: Archiving :: Packaging',
          'Topic :: System :: Software Distribution',
      ],
      keywords='Pip Requirements Setuptools Distutils',
      packages=find_packages(exclude=('tests',)),
      entry_points={
          'distutils.setup_keywords': [
              'reqfiles = reqfiles.setuptools:reqfiles'
          ]
      },
      **reqfiles.Reqfiles())
