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
            EC2Manager(data_type)

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_printable_representation_is_type_string(self, account):
        assert type(repr(account.ec2)) == str

    # ---------------------------------------------------------------------------- #

    def test_ec2_manager_instance_to_dict_is_type_dict(self, account):
        assert type((account.ec2.to_dict())) == dict
