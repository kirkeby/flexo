#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
    name='flexo',
    description='A friendly IRC bot',
    version='0.1',
    packages=find_packages('.'),
    package_dir = {'':'.'},
)
