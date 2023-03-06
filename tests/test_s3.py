from moto import mock_s3, mock_sts
import pytest
import logging

from tests.constants import BUCKETS


# Add a logger module to reduce the repeated code
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@mock_sts
@mock_s3
def prepare_s3_environment(s):
    """Prepare the S3 environment for testing"""

    logger.info("Preparing S3 environment")
    for b in BUCKETS:
        s._session.client("s3").create_bucket(Bucket=b)
        logger.debug("Bucket created: %s", b)

# ---------------------------------------------------------------------------- #

@pytest.mark.s3
@mock_s3
@mock_sts
class TestS3:
    """Testing class for S3"""

    # @pytest.mark.xfail
    @pytest.mark.wip
    def test_list_buckets(self, session):
        # Prepare the S3 environment prior to testing
        prepare_s3_environment(session)
        
        logger.info("Testing ability to list account buckets")
        
        s = session
        buckets = s._session.client("s3").list_buckets()["Buckets"]
        
        logger.debug("Buckets(%s): %s", len(buckets), [b["Name"] for b in buckets])

        assert isinstance(buckets, list)
        assert len(buckets) == len(BUCKETS)

        for b in buckets:
            assert b["Name"] in BUCKETS