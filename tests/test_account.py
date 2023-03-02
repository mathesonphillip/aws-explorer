import os
from json import dumps

from moto import mock_ec2, mock_sts
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
    @fixture(autouse=True)
    def account(self, monkeypatch, credentials_path):
        monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", credentials_path.as_posix())
        print("Monkeypatched AWS_SHARED_CREDENTIALS_FILE")

        _account = Account(profile="aws-exporter", region="ap-southeast-2")

        yield _account

    # @fixture(scope="class")
    # def account(self):
    #     yield Account(profile="aws-exporter", region="ap-southeast-2")

    # ---------------------------------------------------------------------------- #
    def test_account_can_create_with_named_profile(self, account):
        assert account.session.profile_name == "aws-exporter"
        assert "AWSEXPORTER" in account.session.get_credentials().access_key
        assert "AWSEXPORTER" in account.session.get_credentials().secret_key

    # ---------------------------------------------------------------------------- #

    def test_account_is_type_account(self, account):
        assert isinstance(account, Account)

    def test_account_contains_service_managers(self, account):
        assert isinstance(account.ec2, EC2Manager)
        assert isinstance(account.iam, IAMManager)
        assert isinstance(account.s3, S3Manager)
        assert isinstance(account.sts, STSManager)
        assert isinstance(account.cf, CloudFormationManager)
        assert isinstance(account.backup, BackupManager)
        assert isinstance(account.lamb, LambdaManager)
        assert isinstance(account.ecs, ECSManager)
