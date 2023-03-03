import os

import pytest
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
# Fixture that creates a temporary credentials file and returns the path
@pytest.fixture(scope="session")
def credentials_path(tmp_path_factory):
    """Create a temporary credentials file and return the path."""
    path = tmp_path_factory.mktemp("data") / "credentials"
    path.write_text(CREDENTIALS_CONTENT)
    yield path


@pytest.fixture(autouse=True)
def account(monkeypatch, credentials_path):
    """Mocked AWS Credentials for moto."""
    # Ovewrite the environment variables with fail-safe values
    os.environ["AWS_ACCESS_KEY_ID"] = "aws-exporter"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "aws-exporter"
    os.environ["AWS_SECURITY_TOKEN"] = "aws-exporter"
    os.environ["AWS_SESSION_TOKEN"] = "aws-exporter"
    os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"

    # Monkeypatch the environment variables for AWS_SHARED_CREDENTIALS_FILE for fail-safe
    monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", credentials_path.as_posix())
    print("Monkeypatched AWS_SHARED_CREDENTIALS_FILE")

    # Monkeypatch envvar for MOTO_ACCOUNT_ID, so i know what im testing
    monkeypatch.setenv("MOTO_ACCOUNT_ID", "111111111111")

    _account = Account(profile="aws-exporter", region="ap-southeast-2")

    yield _account
