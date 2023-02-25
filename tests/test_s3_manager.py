import boto3
from moto import mock_s3
from aws_explorer import S3Manager


@mock_s3
def test_s3_manager():
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="my-bucket",
        CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
    )
    account = S3Manager(boto3.Session())
    assert len(account.buckets) == 1
