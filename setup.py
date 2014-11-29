#!/usr/bin/env python
import imp
import sys
import os

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import find_packages, setup

root = os.path.dirname(os.path.realpath(__file__))
description = "Farm economy model"
with open(os.path.join(root, 'README.md')) as readme:
    long_description = readme.read()

setup(
    name="farm_econommy",
    version=0.1,
    author="Terry Stewart and Kirsten Robinson",
    author_email="k.w.robinson@gmail.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'farm_econommy = farm_econommy:main',
        ]
    },
    scripts=[],
    description=description,
    long_description=long_description,
    requires=[
    ],
)
