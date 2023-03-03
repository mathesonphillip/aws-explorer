import os
from json import dumps

from moto import mock_ec2, mock_sts
import pytest

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
    def test_account_create_with_named_profile(self, account):
        assert account.session.profile_name == "aws-exporter"
        assert "AWSEXPORTER" in account.session.get_credentials().access_key
        assert "AWSEXPORTER" in account.session.get_credentials().secret_key

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
