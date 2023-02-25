# import boto3
from moto import mock_ec2

# from aws_explorer import EC2Manager
# from random import choice


@mock_ec2
def test_ec2_manager():
    # ec2 = boto3.client("ec2")
    # ec2
    assert 1 == 1

    # Select random image from the list of available images
    # image_id = choice(ec2.describe_images()["Images"]).get("ImageId")

    # print(image_id)

    # ec2.run_instances(ImageId=image_id, InstanceType="t2.micro", MaxCount=1, MinCount=1)

    # account = EC2Manager(boto3.Session())

    # print(account.instances)

    # assert len(account.instances) == 1
