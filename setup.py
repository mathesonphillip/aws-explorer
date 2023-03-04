#!/usr/bin/env python
# """
# Standard setup.py file for Python packages.
# Still learning how to do this properly, so this is a work in progress.
# """
from setuptools import find_packages, setup

# with open("requirements.txt", "r") as fh:
#     requirements = fh.read()

setup(
    name="aws_explorer",
    version="0.1.0",
    description="A Python package to explore AWS resources",
    author="Phillip Matheson",
    url="https://github.com/mathesonphillip/aws-explorer",
    author_email="matheson.phillip@gmail.com",
    packages=find_packages(),
    # install_requires=[
    #     "boto3==1.24.28",
    #     "deepmerge==1.1.0",
    #     "moto==4.1.3",
    #     "mypy_boto3_backup==1.26.67",
    #     "mypy_boto3_rds==1.26.72",
    #     "mypy-boto3-backup==1.26.67",
    #     "mypy-boto3-cloudformation==1.26.60",
    #     "mypy-boto3-cloudtrail==1.26.72",
    #     "mypy-boto3-cloudwatch==1.26.52",
    #     "mypy-boto3-config==1.26.18",
    #     "mypy-boto3-dynamodb==1.26.24",
    #     "mypy-boto3-ec2==1.26.81",
    #     "mypy-boto3-ecs==1.26.78",
    #     "mypy-boto3-iam==1.26.62",
    #     "mypy-boto3-lambda==1.26.80",
    #     "mypy-boto3-logs==1.26.53",
    #     "mypy-boto3-rds==1.26.72",
    #     "mypy-boto3-s3==1.26.62",
    #     "mypy-boto3-ssm==1.26.77",
    #     "mypy-boto3-sts==1.26.57",
    #     "mypy-extensions==1.0.0",
    #     "pandas-stubs==1.5.3.230227",
    #     "pandas==1.5.3",
    #     "pytest==7.2.1",
    #     "PyYAML==6.0",
    #     "setuptools==65.5.0",
    #     "types-PyYAML==6.0.12.8",
    # ],
)
