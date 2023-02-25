from moto import mock_sts, mock_iam, mock_s3, mock_ec2
from aws_explorer import Account


@mock_s3
@mock_ec2
@mock_iam
@mock_sts
def test_account_creation():
    account = Account()
    assert account is not None
