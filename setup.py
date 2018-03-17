#!/usr/bin/env python3
from setuptools import setup, find_packages
import sys

if sys.version_info < (3,5):
        raise Exception("This program only supports Python 3.5 or later.")

setup(  name="apt-sourcemgr",
        version="0.1",
        install_requires=[
                "python-apt",
                "PyYAML",
                "Jinja2",
        ],
        author="Jens John",
        author_email="dev@2ion.de",
        packages=find_packages(exclude=['apt']),
        include_package_data=True,
        description="CLI around python-apt for simple APT sources.list entry management",
        license="GPL3",
        keywords="apt dpkg sources.list",
        entry_points={
                'console_scripts':[
                        'apt-sourcemgr = apt.sourcemgr.__main__:main',
                        'bash_completion_gen_apt_sourcemgr = apt.sourcemgr.bash_completion:main'
                ]
        },
        url="https://github.com/BunsenLabs/bunsen-sourcemgr",
)
