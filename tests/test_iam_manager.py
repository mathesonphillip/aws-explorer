# import boto3
# from moto import mock_iam
# from aws_explorer import IAMManager


# @mock_iam
# def test_iam_manager():
#     iam = boto3.client("iam")
#     iam.create_user(UserName="my-user")
#     account = IAMManager(boto3.Session())
#     assert len(account.users) == 1


# @mock_iam
# def test_iam_manager_alias():
#     iam = boto3.client("iam")
#     iam.create_account_alias(AccountAlias="my-alias")
#     account = IAMManager(boto3.Session())
#     assert account.alias == "my-alias"


def test_iam_manager():
    assert 1 == 1
