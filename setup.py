#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='plug',
    version='0.1.0',
    description='A tool for creating pluggable web-processes for deployment ',
    keywords = 'deployment packaging',
    url='https://github.com/philipcristiano/plug',
    author='Philip Cristiano',
    author_email='plug@philipcristiano.com',
    license='BSD',
    packages=['plug'],
    install_requires=[''],
    test_suite='tests',
    long_description=read('README.rst'),
    zip_safe=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
    entry_points="""
    [console_scripts]
    plug_create = plug.cmd:create
    plug_install = plug.cmd:install
    """

)
