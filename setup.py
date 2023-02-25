#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="aws_explorer",
    version="0.1.0",
    description="A Python package to explore AWS resources",
    author="Phillip Matheson",
    url="https://github.com/mathesonphillip/aws-explorer",
    author_email="matheson.phillip@gmail.com",
    packages=find_packages(),
    install_requires=[
        "boto3==1.24.28",
        "moto==4.1.3",
        "setuptools==65.5.0",
    ],
)
