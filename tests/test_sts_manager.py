import boto3
from moto import mock_sts
from aws_explorer import STSManager
import pytest
import os

os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"


@mock_sts
class TestSTSManager:
    # --------------------------------------------------------------------------- #

    @pytest.mark.parametrize("key", ["access_key", "secret_key"])
    def test_sts_manager_session_has_access_key_and_secret_key(self, key):
        sts = STSManager(boto3.Session())
        session_credentials = sts.session.get_credentials()
        print(session_credentials)
        assert getattr(session_credentials, key) is not None

    # ---------------------------------------------------------------------------- #

    @pytest.mark.parametrize("data_type", [1, 1.0, True, None, [], {}])
    def test_sts_manager_should_fail_when_not_given_correct_data_type_for_session_param(
        self, data_type
    ):
        with pytest.raises(AttributeError):
            sts = STSManager(data_type)

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_should_fail_when_not_given_str_for_session_param(self):
        with pytest.raises(AttributeError):
            sts = STSManager("session")

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_should_fail_when_missing_session_param(self):
        with pytest.raises(TypeError):
            sts = STSManager()

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_is_not_none(self):
        sts = STSManager(boto3.Session())
        assert sts is not None

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_session_is_not_none(self):
        sts = STSManager(boto3.Session())
        assert sts.session is not None

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_instance_variable_is_not_none(self):
        sts = STSManager(boto3.Session())
        assert sts.identity is not None

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_printable_representation_is_type_string(self):
        sts = STSManager(boto3.Session())
        assert type(repr(sts)) == str

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_identity_var_is_type_dict(self):
        session = boto3.Session()
        sts = STSManager(session)

        print(f"{sts.identity}, {type(sts.identity)}")

        assert type(sts.identity) == dict

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_instance_to_dict_is_type_dict(self):
        session = boto3.Session()
        sts = STSManager(session)
        assert type(sts.to_dict()) == dict
