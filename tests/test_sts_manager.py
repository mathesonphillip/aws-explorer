import pytest
from moto import mock_sts

from aws_explorer import STSManager


@mock_sts
class TestSTSManager:
    # --------------------------------------------------------------------------- #

    @pytest.mark.parametrize("data_type", [1, 1.0, True, None, [], {}])
    def test_sts_manager_should_fail_when_not_given_correct_data_type_for_session_param(
        self, data_type
    ):
        with pytest.raises(AttributeError):
            STSManager(data_type)

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_instance_variable_is_not_none(self, account):
        assert account.sts.identity is not None

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_printable_representation_is_type_string(self, account):
        assert type(repr(account.sts)) == str

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_identity_var_is_type_dict(self, account):
        assert type(account.sts.identity) == dict

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_instance_to_dict_is_type_dict(self, account):
        assert type(account.sts.to_dict()) == dict
