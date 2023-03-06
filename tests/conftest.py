import logging
import pytest
from aws_explorer.session import Session

from tests.constants import CREDENTIAL_FILE_CONTENTS, PROFILE
# ---------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# ---------------------------------------------------------------------------- #

@pytest.fixture(scope="session")
def credentials_path(tmp_path_factory):
    """Create a temporary credentials file and return the path."""

    logger.info("Generating temporary credentials file")

    path = tmp_path_factory.mktemp("data") / "credentials"
    path.write_text(CREDENTIAL_FILE_CONTENTS)

    yield path

    logger.info("Finished with temporary credentials file")

@pytest.fixture()
def session(monkeypatch, credentials_path):
    """
    Create a session using the mocked credentials file
    Where applicable all tests should use this fixture to ensure mock credentials are used.
    """

    logger.warning("Using mocked AWS Credentials")

    # Monkeypatch the environment variables for AWS_SHARED_CREDENTIALS_FILE for fail-safe
    monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", credentials_path.as_posix())

    # Create the session
    session = Session(profile=PROFILE, region="us-east-1")
    
    yield session

    logger.info("Finished with mocked AWS Credentials")
