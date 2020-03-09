# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "api"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="XYK token swap API",
    author_email="vanderka.marian@gmail.com",
    url="",
    keywords=["Swagger", "XYK token swap API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    long_description="""\
    REST API spec for XYK token swap
    """
)
