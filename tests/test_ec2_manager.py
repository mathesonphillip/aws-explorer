from moto import mock_ec2
from pytest import mark, raises

from aws_explorer import EC2Manager


@mock_ec2
# @mark.ec2
class TestEC2Manager:
    @mark.parametrize("data_type", [1, 1.0, True, None, "Session", [], {}])
    def test_ec2_manager_should_fail_when_not_given_correct_data_type_for_session_param(
        self, data_type
    ):
        with raises(AttributeError):
            ec2 = EC2Manager(data_type)

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_is_not_none(self, session):
        ec2 = EC2Manager(session)
        assert ec2 is not None

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_instance_variable_is_not_none(self, session):
        ec2 = EC2Manager(session)
        assert ec2.instances is not None

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_printable_representation_is_type_string(self, session):
        ec2 = EC2Manager(session)
        assert type(repr(ec2)) == str

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_instance_var_is_type_list(self, session):
        ec2 = EC2Manager(session)
        assert ec2.instances == list

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_instance_to_dict_is_type_dict(self, session):
        ec2 = EC2Manager(session)
        assert type((ec2.to_dict())) == dict
