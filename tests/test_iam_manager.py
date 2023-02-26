from moto import mock_iam
from pytest import mark, raises

from aws_explorer import IAMManager


@mock_iam
# @mark.iam
class TestIAMManager:
    # --------------------------------------------------------------------------- #

    @mark.parametrize("data_type", [1, 1.0, True, None, "Session", [], {}])
    def test_iam_manager_should_fail_when_not_given_correct_data_type_for_session_param(
        self, data_type
    ):
        with raises(AttributeError):
            IAMManager(data_type)

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_is_not_none(self, account):
        assert account.iam is not None

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_session_is_not_none(self, account):
        assert account.iam.session is not None

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_instance_variable_is_not_none(self, account):
        assert account.iam.users is not None

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_printable_representation_is_type_string(self, account):
        assert type(repr(account.iam)) == str

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_identity_var_is_type_list(self, account):
        assert type(account.iam.users) == list

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_instance_to_dict_is_type_dict(self, account):
        assert type(account.iam.to_dict()) == dict
