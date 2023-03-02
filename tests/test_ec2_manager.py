from moto import mock_ec2
import pytest

from aws_explorer import Account, EC2Manager


@mock_ec2
# @mark.ec2
class TestEC2Manager:
    @pytest.fixture(autouse=True)
    def account(self, monkeypatch, credentials_path):
        monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", credentials_path.as_posix())
        print("Monkeypatched AWS_SHARED_CREDENTIALS_FILE")

        _account = Account(profile="aws-exporter", region="ap-southeast-2")

        yield _account

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_printable_representation_is_type_string(self, account):
        assert isinstance(repr(account.ec2), str)

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_instance_to_dict_is_type_dict(self, account):
        assert isinstance(account.ec2.to_dict(), dict)
