#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='simplesignals',
    version='0.3.0',
    description='Unix signal handlers and worker processes, simplified',
    author='Jamie Matthews',
    author_email='jamie.matthews@gmail.com',
    url='https://github.com/j4mie/simplesignals',
    license = 'Public Domain',
    packages=find_packages(),
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: Unix",
    ],
)
