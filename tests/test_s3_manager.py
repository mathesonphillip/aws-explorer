from moto import mock_s3
import pytest


@mock_s3
class TestS3Manager:
    def test_s3_to_dict(self, account):
        response: dict = account.s3.to_dict()
        assert isinstance(response, dict)
        assert isinstance(response["Buckets"], list)

    def test_s3_buckets(self, account):
        response = account.s3.buckets
        assert isinstance(response, list)
