from moto import mock_sts
import pytest
import logging
import os
from aws_explorer.session import Session, InvalidSessionConfigError


from tests.constants import CREDENTIALS, ACCOUNT_ID, TEST_PARAMS


# ---------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------- #


@mock_sts
@pytest.mark.session
class TestSession:
    """Test the Session class."""

    @pytest.mark.parametrize("expected, profile, region, access_key, secret_key", TEST_PARAMS["test_session_init"])
    def test_session_init(self, credentials_path, expected, profile, region, access_key, secret_key):
        """
        Test scenarios for creating a session
        Only need to test all scenarios in this test case.
        All other test cases will use the session fixture to ensure consistency.
        """

        # Ovewrite the environment variables with fail-safe values
        os.environ["AWS_ACCESS_KEY_ID"] = CREDENTIALS.access_key
        os.environ["AWS_SECRET_ACCESS_KEY"] = CREDENTIALS.secret_key
        os.environ["AWS_SHARED_CREDENTIALS_FILE"] = credentials_path.as_posix()

        if expected is not InvalidSessionConfigError:
            s = Session(profile, region, access_key, secret_key)

            logger.debug(s)
            logger.debug(s.credentials)
            logger.debug(s.identity)

            assert s.config.profile == expected
            assert s.identity.account_id == ACCOUNT_ID
            assert s.credentials.access_key == CREDENTIALS.access_key
            assert s.credentials.secret_key == CREDENTIALS.secret_key

        else:
            # Testing for InvalidSessionConfigError
            with pytest.raises(InvalidSessionConfigError):
                Session(profile, region, access_key, secret_key)

    def test_session_is_mock(self, session):
        """Test creating a session with no credentials"""

        s = session

        logger.debug(s.config)
        logger.debug(s.credentials)
        logger.debug(s.identity)

        assert s.identity.account_id == ACCOUNT_ID
        assert s.credentials.access_key == CREDENTIALS.access_key
        assert s.credentials.secret_key == CREDENTIALS.secret_key

    def test_session_repr(self, session):
        """Test the __repr__ method"""

        logger.info("Checking the session repr")

        s: Session = session
        s_repr = repr(s)
        excepted_repr = f"<Session session={s.config.profile}, services={s.services}>"

        logger.info(s_repr)

        # logger.debug(s_repr)
        # logger.debug(excepted_repr)

        assert isinstance(s_repr, str)
        assert s_repr == excepted_repr


    @pytest.mark.wip
    @pytest.mark.session
    def test_session_services(self, session):
        """
        Checks that the session has a list of available resource services
        Checks that each service has a resource client
        """

        logger.info("Checking the session has a list of service clients")

        s: Session = session
        assert s.identity.account_id == ACCOUNT_ID

        logger.info(f"Services: {[service.name for service in s.services]}")

        for service in s.services:
            # Check that each available service has a client
            assert "client" in service.service_type.__dir__()
            # Check that each available service has a session
            # TODO: Not actually sure if each service has a session 
            assert "session" in service.service_type.__dir__()