#!/usr/bin/env python

from setuptools import find_packages, setup

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
        "deepmerge==1.1.0",
        "moto==4.1.3",
        "mypy_boto3_backup==1.26.67",
        "mypy_boto3_rds==1.26.72",
        "pandas==1.5.3",
        "pytest==7.2.1",
        "PyYAML==6.0",
        "setuptools==65.5.0",
    ],
)
