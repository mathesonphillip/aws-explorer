import os

import boto3
import pytest
from moto import mock_ec2

from aws_explorer import EC2Manager

os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"


@mock_ec2
class TestEC2Manager:
    # @pytest.mark.parametrize("key", ["access_key", "secret_key"])
    # def test_ec2_manager_session_has_access_key_and_secret_key(self, key):
    #     ec2 = EC2Manager(boto3.Session())
    #     session_credentials = ec2.session.get_credentials()
    #     assert getattr(session_credentials, key) is not None

    # ---------------------------------------------------------------------------- #

    @pytest.mark.parametrize("data_type", [1, 1.0, True, None, [], {}])
    def test_ec2_manager_should_fail_when_not_given_correct_data_type_for_session_param(
        self, data_type
    ):
        with pytest.raises(AttributeError):
            ec2 = EC2Manager(data_type)

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_should_fail_when_not_given_str_for_session_param(self):
        with pytest.raises(AttributeError):
            ec2 = EC2Manager("session")

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_should_fail_when_missing_session_param(self):
        with pytest.raises(TypeError):
            ec2 = EC2Manager()

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_is_not_none(self):
        ec2 = EC2Manager(boto3.Session())
        assert ec2 is not None

    # ---------------------------------------------------------------------------- #

    # def test_ec2_manager_session_is_not_none(self):
    #     ec2 = EC2Manager(boto3.Session())
    #     assert ec2.session is not None

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_instance_variable_is_not_none(self):
        ec2 = EC2Manager(boto3.Session())
        assert ec2.instances is not None

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_printable_representation_is_type_string(self):
        ec2 = EC2Manager(boto3.Session())
        assert type(repr(ec2)) == str

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_instance_var_is_type_list(self):
        session = boto3.Session()
        ec2 = EC2Manager(session)
        assert ec2.instances == list

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_instance_to_dict_is_type_dict(self):
        session = boto3.Session()
        ec2 = EC2Manager(session)
        assert type((ec2.to_dict())) == dict
