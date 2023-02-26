import os

import boto3
import pytest
from moto import mock_iam

from aws_explorer import IAMManager

os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"


@mock_iam
class TestIAMManager:
    # --------------------------------------------------------------------------- #

    @pytest.mark.parametrize("key", ["access_key", "secret_key"])
    def test_iam_manager_session_has_access_key_and_secret_key(self, key):
        iam = IAMManager(boto3.Session())
        session_credentials = iam.session.get_credentials()
        print(session_credentials)
        assert getattr(session_credentials, key) is not None

    # ---------------------------------------------------------------------------- #

    @pytest.mark.parametrize("data_type", [1, 1.0, True, None, [], {}])
    def test_iam_manager_should_fail_when_not_given_correct_data_type_for_session_param(
        self, data_type
    ):
        with pytest.raises(AttributeError):
            iam = IAMManager(data_type)

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_should_fail_when_not_given_str_for_session_param(self):
        with pytest.raises(AttributeError):
            iam = IAMManager("session")

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_should_fail_when_missing_session_param(self):
        with pytest.raises(TypeError):
            iam = IAMManager()

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_is_not_none(self):
        iam = IAMManager(boto3.Session())
        assert iam is not None

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_session_is_not_none(self):
        iam = IAMManager(boto3.Session())
        assert iam.session is not None

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_instance_variable_is_not_none(self):
        iam = IAMManager(boto3.Session())
        assert iam.users is not None

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_printable_representation_is_type_string(self):
        iam = IAMManager(boto3.Session())
        assert type(repr(iam)) == str

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_identity_var_is_type_list(self):
        session = boto3.Session()
        iam = IAMManager(session)

        print(f"{type(iam.users)}, {type(iam.users)}")

        assert type(iam.users) == list

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_instance_to_dict_is_type_dict(self):
        session = boto3.Session()
        iam = IAMManager(session)
        assert type(iam.to_dict()) == dict
