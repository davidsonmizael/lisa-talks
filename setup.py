#!/bin/usr/env python
import os, subprocess
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def get_description():
    with open("README.md", "r") as f:
        return f.read()

def get_requirements():
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()

setup(
    name='LISA Talks',
    version='0.1',
    author='Davidson Mizael',
    author_email='davidsonmizael@gmail.com',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=get_description(),
    #packages=['core'],
    install_requires=get_requirements()
)