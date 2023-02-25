import boto3
from moto import mock_s3
from aws_explorer import S3Manager
import pytest


@mock_s3
class TestS3Manager:
    # --------------------------------------------------------------------------- #

    @pytest.mark.parametrize("key", ["access_key", "secret_key"])
    def test_s3_manager_session_has_access_key_and_secret_key(self, key):
        s3 = S3Manager(boto3.Session())
        session_credentials = s3.session.get_credentials()
        print(session_credentials)
        assert getattr(session_credentials, key) is not None

    # ---------------------------------------------------------------------------- #

    @pytest.mark.parametrize("data_type", [1, 1.0, True, None, [], {}])
    def test_s3_manager_should_fail_when_not_given_correct_data_type_for_session_param(
        self, data_type
    ):
        with pytest.raises(AttributeError):
            s3 = S3Manager(data_type)

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_should_fail_when_not_given_str_for_session_param(self):
        with pytest.raises(AttributeError):
            s3 = S3Manager("session")

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_should_fail_when_missing_session_param(self):
        with pytest.raises(TypeError):
            s3 = S3Manager()

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_is_not_none(self):
        s3 = S3Manager(boto3.Session())
        assert s3 is not None

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_session_is_not_none(self):
        s3 = S3Manager(boto3.Session())
        assert s3.session is not None

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_instance_variable_is_not_none(self):
        s3 = S3Manager(boto3.Session())

        print(s3.buckets)
        assert s3.buckets is not None

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_printable_representation_is_type_string(self):
        s3 = S3Manager(boto3.Session())
        assert type(repr(s3)) == str

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_bucket_var_is_type_list(self):
        session = boto3.Session()
        s3 = S3Manager(session)

        assert type(s3.buckets) == list

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_instance_to_dict_is_type_dict(self):
        session = boto3.Session()
        s3 = S3Manager(session)
        assert type(s3.to_dict()) == dict
