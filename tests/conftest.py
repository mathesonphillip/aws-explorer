import os

import boto3
import pytest
from faker import Faker

from aws_explorer import Account, EC2Manager, IAMManager, S3Manager

# Initiate Faker
fake = Faker()
Faker.seed(0)

# AWS Credentials (Faker)
AWS_DEFAULT_REGION = "ap-southeast-2"
AWS_ACCESS_KEY_ID = fake.password(length=20, special_chars=False, upper_case=False)
AWS_SECRET_ACCESS_KEY = fake.md5(raw_output=False)
AWS_SECURITY_TOKEN = fake.sha256(raw_output=False)
AWS_SESSION_TOKEN = fake.sha1(raw_output=False)


os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"
# Define fixtures


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
    os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
    os.environ["AWS_SECURITY_TOKEN"] = AWS_SECURITY_TOKEN
    os.environ["AWS_SESSION_TOKEN"] = AWS_SESSION_TOKEN
    os.environ["AWS_DEFAULT_REGION"] = AWS_DEFAULT_REGION


# ---------------------------------------------------------------------------- #
#                                   AWS CREDS                                  #
# ---------------------------------------------------------------------------- #
@pytest.fixture(scope="function")
def aws_session(aws_credentials):
    yield boto3.Session(aws_credentials)


# ---------------------------------------------------------------------------- #
#                                  STSManager                                  #
# ---------------------------------------------------------------------------- #

#
# @pytest.fixture(scope='function')
# def STSManager(aws_session):
#     yield _STSManager(aws_session)


# ---------------------------------------------------------------------------- #
#                                  EC2MANAGER                                  #
# ---------------------------------------------------------------------------- #
@pytest.fixture(scope="function")
def EC2MANAGER(aws_credentials):
    yield EC2Manager(aws_credentials)


# ---------------------------------------------------------------------------- #
#                                  IAMMANAGER                                  #
# ---------------------------------------------------------------------------- #
@pytest.fixture(scope="function")
def IAMMANAGER(aws_credentials):
    yield IAMManager(aws_credentials)


# ---------------------------------------------------------------------------- #
#                                   S3MANAGER                                  #
# ---------------------------------------------------------------------------- #
@pytest.fixture(scope="function")
def S3MANAGER(aws_credentials):
    yield S3Manager(aws_credentials)


# ---------------------------------------------------------------------------- #
#                                    ACCOUNT                                   #
# ---------------------------------------------------------------------------- #
@pytest.fixture(scope="function")
def ACCOUNT(aws_credentials):
    yield Account(aws_credentials)
