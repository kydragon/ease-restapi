#!/usr/bin/env python
# coding=utf-8

import os

try:
    import setuptools

    setup = setuptools.setup
except ImportError:
    setuptools = None
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'CHANGELOG.rst')).read()

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
zip_safe = not on_rtd

version = '0.1'

setup(
    name='ease-restapi',
    version=version,
    description="ease-restapi is a Python package that use 'www.easemob.com' website REST API for you.",
    long_description=README + '\n\n' + NEWS,
    install_requires=['six', 'requests'],
    license='MIT License',
    author='kylinfish',
    author_email='kylinfish@126.com',
    keywords='ease-restapi',
    url='https://bitbucket.org/kylinfish/ease-restapi',
    packages=['ease_restapi.service', 'ease_restapi.sulate', 'ease_restapi.demo'],
    platforms=["any"],
    zip_safe=zip_safe,
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta'
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
    ]
)
