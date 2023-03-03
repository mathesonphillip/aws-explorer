from moto import mock_ec2
import pytest


@mock_ec2
class TestEC2Manager:
    def test_ec2_to_dict(self, account):
        response: dict = account.ec2.to_dict()
        assert isinstance(response, dict)
        assert isinstance(response["Instances"], list)
        assert isinstance(response["SecurityGroups"], list)
        assert isinstance(response["SecurityGroupRules"], list)
        assert isinstance(response["Vpcs"], list)
        assert isinstance(response["Subnets"], list)
        assert isinstance(response["InternetGateways"], list)
        assert isinstance(response["NetworkAcls"], list)
        assert isinstance(response["NetworkInterfaces"], list)
        assert isinstance(response["Volumes"], list)
        assert isinstance(response["Snapshots"], list)
        assert isinstance(response["Images"], list)
