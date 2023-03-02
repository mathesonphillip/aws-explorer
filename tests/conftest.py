import os

from boto3 import Session
from pytest import fixture
from aws_explorer import Account

AWS_DEFAULT_REGION = "ap-southeast-2"

AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

CREDENTIALS_CONTENT = f"""
[default]
aws_access_key_id     = AKIAIOSFOEAWSDEFAULT
aws_secret_access_key = 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
region                = {AWS_DEFAULT_REGION}

[aws-exporter]
aws_access_key_id     = AKIAIOSFOAWSEXPORTER
aws_secret_access_key = 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
region                = {AWS_DEFAULT_REGION}
"""

# ---------------------------------------------------------------------------- #


@fixture(scope="session")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@fixture(scope="session")
def region():
    return AWS_DEFAULT_REGION


@fixture(scope="session")
def access_key():
    return AWS_ACCESS_KEY_ID


@fixture(scope="session")
def secret_key():
    return AWS_SECRET_ACCESS_KEY


@fixture(scope="session")
def credentials_content():
    return CREDENTIALS_CONTENT


# ---------------------------------------------------------------------------- #
# Fixture that creates a temporary credentials file and returns the path
@fixture(scope="session")
def credentials_path(tmp_path_factory):
    """Create a temporary credentials file and return the path."""
    path = tmp_path_factory.mktemp("data") / "credentials"
    path.write_text(CREDENTIALS_CONTENT)
    yield path
