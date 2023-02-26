import os
from json import dumps

from moto import mock_ec2
from pytest import fixture, mark, raises

from aws_explorer import (
    Account,
    BackupManager,
    CloudFormationManager,
    EC2Manager,
    ECSManager,
    IAMManager,
    LambdaManager,
    S3Manager,
    STSManager,
)


class TestAccount:
    def test_account_can_create_with_no_profile(
        self,
        monkeypatch,
        credentials_path,
    ):
        # Mock the AWS_DEFAULT_REGION env var
        monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", credentials_path.as_posix())

        account = Account()
        assert account.session.profile_name == "default"
        assert "AWSDEFAULT" in account.session.get_credentials().access_key
        assert "AWSDEFAULT" in account.session.get_credentials().secret_key

    # ---------------------------------------------------------------------------- #
    def test_account_can_create_with_named_profile(
        self,
        monkeypatch,
        credentials_path,
    ):
        # Mock the AWS_DEFAULT_REGION env var
        monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", credentials_path.as_posix())

        account = Account(profile_name="aws-exporter")
        assert account.session.profile_name == "aws-exporter"
        assert "AWSEXPORTER" in account.session.get_credentials().access_key
        assert "AWSEXPORTER" in account.session.get_credentials().secret_key

    # ---------------------------------------------------------------------------- #

    def test_account_can_create_with_credentials_dict(self, credentials):
        account = Account(credentials=credentials)
        assert account.session.profile_name == "default"
        assert "EXAMPLE" in account.session.get_credentials().access_key
        assert "EXAMPLEKEY" in account.session.get_credentials().secret_key

    # ---------------------------------------------------------------------------- #

    def test_account_is_type_account(self, account):
        assert type(account) == Account

    def test_account_contains_service_managers(self, account):
        assert type(account.ec2) == EC2Manager
        assert type(account.iam) == IAMManager
        assert type(account.s3) == S3Manager
        assert type(account.sts) == STSManager
        assert type(account.cf) == CloudFormationManager
        assert type(account.backup) == BackupManager
        assert type(account.lamb) == LambdaManager
        assert type(account.ecs) == ECSManager
