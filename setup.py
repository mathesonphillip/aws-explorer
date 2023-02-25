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
        "boto3 == 1.24.28",
        "Faker == 17.3.0",
        "moto == 4.1.3",
        "pytest == 7.2.1",
        "setuptools == 65.5.0",
    ],
)
