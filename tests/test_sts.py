import pytest
from moto import mock_sts
# from aws_explorer.session import Session

from tests.constants import ACCOUNT_ID

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@mock_sts
class TestSTSManager:
    
    @pytest.mark.sts
    @pytest.mark.wip
    def test_sts_identity(self, session):
        assert session.sts.identity.account_id == ACCOUNT_ID
        assert session.sts.identity.user_id == "AKIAIOSFODNN7EXAMPLE"
        assert session.sts.identity.arn == "arn:aws:sts::123456789012:user/moto"

    @pytest.mark.sts
    @pytest.mark.wip
    def test_sts_repr(self, session):
        """Test the __repr__ method"""

        excepted_repr = f"<STSManager session={session.config.profile}>"

        


        logger.debug(repr(session.sts))
        logger.debug(excepted_repr)

        assert repr(session.sts) == excepted_repr