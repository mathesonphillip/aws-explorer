import os

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
def region():
    return AWS_DEFAULT_REGION


@fixture(scope="session")
def access_key():
    return AWS_ACCESS_KEY_ID


@fixture(scope="session")
def secret_key():
    return AWS_SECRET_ACCESS_KEY


@fixture(scope="session")
def credentials(region, access_key, secret_key):
    credentials = {
        "region_name": region,
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
    }

    yield credentials


# ---------------------------------------------------------------------------- #
@fixture(scope="session")
def account(credentials):
    yield Account(credentials=credentials, region_name=AWS_DEFAULT_REGION)


# Fixture that creates a temporary credentials file and returns the path
@fixture(scope="session")
def credentials_path(tmp_path_factory):
    """Create a temporary credentials file and return the path."""
    path = tmp_path_factory.mktemp("data") / "credentials"
    path.write_text(CREDENTIALS_CONTENT)
    yield path
