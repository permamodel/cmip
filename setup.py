#! /usr/bin/env python
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages


setup(name='cmip',
      version='0.1',
      author='J Scott Stewart',
      author_email='james.stewart@colorado.edu',
      description='cmip',
      long_description=open('README.md').read(),
      packages=find_packages(),
      install_requires=('numpy', 'nose', 'netcdf4', 'pyyaml',
                        'python-dateutil'),
      package_data={'': ['examples/*', 'data/*']}
)
