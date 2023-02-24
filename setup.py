#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="aws_explorer",
    version="0.1.0",
    description="A Python package to explore AWS resources",
    author="Phillip Matheson",
    author_email="matheson.phillip@gmail.com",
    packages=find_packages(),
    install_requires=["boto3==1.24.28"],
)
