#!/usr/bin/env python3
from setuptools import setup
from apt.sourcemgr import version

setup(  name="apt-sourcemgr",
        version=version,
        scripts=["apt-sourcemgr"],
        install_requires=["python-apt"],
        author="Jens John",
        author_email="dev@2ion.de",
        description="CLI around python-apt for simple APT sources.list entry management",
        license="GPL3",
        keywords="apt dpkg sources.list",
        url="https://github.com/BunsenLabs/bunsen-sourcemgr",
)
