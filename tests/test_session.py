from moto import mock_sts
import pytest
import logging
import os
from aws_explorer.session import Session, InvalidSessionConfigError, Credentials, Profile


from tests.constants import CREDENTIALS, ACCOUNT_ID, TEST_PARAMS


# ---------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------- #


@mock_sts
@pytest.mark.session
class TestSession:

    """Test the Session class."""

    @pytest.mark.parametrize(
        "expected, session_configuration",
        [
            ("default", Profile(profile_name=None)),
            ("explorer", Profile(profile_name="explorer")),
            ("default", Profile(region_name="ap-southeast-2")),
            ("default", Profile(region_name="us-east-1")),
            ("explorer", Profile(profile_name="explorer", region_name="ap-southeast-2")),
        ],
    )
    def test_session_init(self, credentials_path, expected, session_configuration):
        """Test scenarios for creating a session.

        Only need to test all scenarios in this test case.
        All other test cases will use the session fixture to ensure consistency.
        """

        os.environ["AWS_ACCESS_KEY_ID"] = CREDENTIALS.access_key
        os.environ["AWS_SECRET_ACCESS_KEY"] = CREDENTIALS.secret_key
        os.environ["AWS_SHARED_CREDENTIALS_FILE"] = credentials_path.as_posix()

        s = Session(session_configuration)

        assert s._session.profile_name == expected
