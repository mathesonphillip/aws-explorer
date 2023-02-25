import boto3
from moto import mock_sts
from aws_explorer import STSManager


@mock_sts
def test_sts_manager():
    sts = boto3.client("sts")
    identity = sts.get_caller_identity()
    del identity["ResponseMetadata"]

    account = STSManager(boto3.Session())

    print(account.identity)
    print(identity)
    assert account.identity == identity
