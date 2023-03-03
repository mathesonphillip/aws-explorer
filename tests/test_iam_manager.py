from moto import mock_iam
import pytest


@mock_iam
class TestIAMManager:
    def test_iam_to_dict(self, account):
        response: dict = account.iam.to_dict()
        assert isinstance(response, dict)
        assert isinstance(response["Users"], list)
        assert isinstance(response["Groups"], list)
        assert isinstance(response["Roles"], list)
        assert isinstance(response["Policies"], list)
