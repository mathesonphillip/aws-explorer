from moto import mock_s3
from pytest import mark, raises

from aws_explorer import S3Manager


@mock_s3
# @mark.s3
class TestS3Manager:
    @mark.parametrize("data_type", [1, 1.0, True, None, [], {}])
    def test_s3_manager_should_fail_when_not_given_correct_data_type_for_session_param(
        self, data_type
    ):
        with raises(AttributeError):
            s3 = S3Manager(data_type)

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_is_not_none(self, session):
        s3 = S3Manager(session)
        assert s3 is not None

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_instance_variable_is_not_none(self, session):
        s3 = S3Manager(session)

        print(s3.buckets)
        assert s3.buckets is not None

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_printable_representation_is_type_string(self, session):
        s3 = S3Manager(session)
        assert type(repr(s3)) == str

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_bucket_var_is_type_list(self, session):
        session = session
        s3 = S3Manager(session)

        assert type(s3.buckets) == list

    # ---------------------------------------------------------------------------- #

    def test_s3_manager_instance_to_dict_is_type_dict(self, session):
        session = session
        s3 = S3Manager(session)
        assert type(s3.to_dict()) == dict
