#!/bin/usr/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools.command.develop import develop
from setuptools.command.install import install
from dotenv import load_dotenv
from scripts import generate_pickle
from scripts import generate_models
from scripts import test_model

#loading .env properties
load_dotenv(".env")

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        generate_pickle.generate()
        generate_models.generate()
        test_model.test()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        generate_pickle.generate()
        generate_models.generate()
        test_model.test()


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
    install_requires=get_requirements(),
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)