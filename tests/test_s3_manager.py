from moto import mock_s3
import pytest

from aws_explorer import Account, S3Manager


@mock_s3
# @mark.s3
class TestS3Manager:
    @pytest.fixture(autouse=True)
    def account(self, monkeypatch, credentials_path):
        monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", credentials_path.as_posix())
        print("Monkeypatched AWS_SHARED_CREDENTIALS_FILE")

        _account = Account(profile="aws-exporter", region="ap-southeast-2")

        yield _account

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_is_not_none(self, account):
        assert account.s3 is not None

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_instance_variable_is_not_none(self, account):
        assert account.s3.buckets is not None

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_printable_representation_is_type_string(self, account):
        assert type(repr(account.s3)) == str

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_bucket_var_is_type_list(self, account):
        assert type(account.s3.buckets) == list

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_instance_to_dict_is_type_dict(self, account):
        assert type(account.s3.to_dict()) == dict
