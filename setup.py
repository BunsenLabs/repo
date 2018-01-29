#!/usr/bin/env python3
from setuptools import setup

setup(  name="apt-sourcemgr",
        version="0.1.0",
        scripts=["apt-sourcemgr"],
        install_requires=["python-apt"],
        author="Jens John",
        author_email="dev@2ion.de",
        description="CLI around python-apt for simple APT sources.list entry management",
        license="GPL3",
        keywords="apt dpkg sources.list",
        url="https://github.com/BunsenLabs/bunsen-sourcemgr",
)
