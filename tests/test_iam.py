from moto import mock_iam
import pytest

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@mock_iam
class TestIAM:

    @pytest.mark.iam
    @pytest.mark.wip
    def test_iam_repr(self, session):
        """Test the __repr__ method"""

        excepted_repr = f"<IAMManager session={session.config.profile}>"

        logger.debug(repr(session.iam))
        logger.debug(excepted_repr)

        assert repr(session.iam) == excepted_repr
