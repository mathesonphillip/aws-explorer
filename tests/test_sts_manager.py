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
            sts = STSManager(data_type)

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_instance_variable_is_not_none(self, session):
        sts = STSManager(session)
        assert sts.identity is not None

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_printable_representation_is_type_string(self, session):
        sts = STSManager(session)
        assert type(repr(sts)) == str

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_identity_var_is_type_dict(self, session):
        session = session
        sts = STSManager(session)

        print(f"{sts.identity}, {type(sts.identity)}")

        assert type(sts.identity) == dict

    # ---------------------------------------------------------------------------- #

    def test_sts_manager_instance_to_dict_is_type_dict(self, session):
        session = session
        sts = STSManager(session)
        assert type(sts.to_dict()) == dict
