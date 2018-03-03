#!/usr/bin/env python3
from setuptools import setup, find_packages
from apt.sourcemgr import VERSION
import sys

if sys.version_info < (3,5):
        raise Exception("This program only supports Python 3.5 or later.")

setup(  name="apt-sourcemgr",
        version=VERSION,
        scripts=["apt-sourcemgr"],
        install_requires=["python-apt"],
        author="Jens John",
        author_email="dev@2ion.de",
        packages=find_packages(exclude=['apt']),
        include_package_data=True,
        description="CLI around python-apt for simple APT sources.list entry management",
        license="GPL3",
        keywords="apt dpkg sources.list",
        url="https://github.com/BunsenLabs/bunsen-sourcemgr",
)
