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
            iam = IAMManager(data_type)

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_should_fail_when_not_given_str_for_session_param(self):
        with raises(AttributeError):
            iam = IAMManager("session")

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_should_fail_when_missing_session_param(self):
        with raises(TypeError):
            iam = IAMManager()

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_is_not_none(self, session):
        iam = IAMManager(session)
        assert iam is not None

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_session_is_not_none(self, session):
        iam = IAMManager(session)
        assert iam.session is not None

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_instance_variable_is_not_none(self, session):
        iam = IAMManager(session)
        assert iam.users is not None

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_printable_representation_is_type_string(self, session):
        iam = IAMManager(session)
        assert type(repr(iam)) == str

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_identity_var_is_type_list(self, session):
        session = session
        iam = IAMManager(session)

        print(f"{type(iam.users)}, {type(iam.users)}")

        assert type(iam.users) == list

    # ---------------------------------------------------------------------------- #

    def test_iam_manager_instance_to_dict_is_type_dict(self, session):
        session = session
        iam = IAMManager(session)
        assert type(iam.to_dict()) == dict
