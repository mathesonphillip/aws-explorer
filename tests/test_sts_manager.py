import pytest
from moto import mock_sts


@mock_sts
class TestSTSManager:
    def test_sts_to_dict(self, account):
        response: dict[str, dict] = account.sts.to_dict()
        assert isinstance(response, dict)

    def test_account_sts_identity(self, account):
        response = account.sts.get_identity
        assert response["Account"] == "111111111111"
        assert response["UserId"] == "AKIAIOSFODNN7EXAMPLE"
        assert response["Arn"] == "arn:aws:sts::111111111111:user/moto"
