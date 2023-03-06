"""Class module for the EC2Manager class, which is used to interact with the AWS EC2 service."""


import boto3

from .utils import filter_and_sort_dict_list


class EC2Manager:

    """This class is used to manage EC2 resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("ec2")

    @property
    def instances(self) -> list[dict]:
        """Return a list of EC2 instances."""
        result: list[dict] = []
        for res in self.client.describe_instances()["Reservations"]:
            for j in res.get("Instances", []):
                _instance: dict = {
                    "session": self.session.profile_name,
                    "Name": None,
                    "SSMManaged": False,
                    "VpcName": False,
                    "SubnetName": False,
                    **j,
                }

                for tag in j.get("Tags", []):
                    if tag.get("Key") == "Name":
                        _instance["Name"] = tag.get("Value")

                for _ssm in self.session.client("ssm").describe_instance_information().get("InstanceInformationList", []):
                    if _ssm.get("InstanceId") == j.get("InstanceId"):
                        _instance["SSMManaged"] = True

                for _vpc in self.vpcs:
                    if _vpc.get("VpcId") == j.get("VpcId"):
                        _instance["VpcName"] = _vpc.get("Name")

                for _sub in self.subnets:
                    if _sub.get("SubnetId") == j.get("SubnetId"):
                        _instance["SubnetName"] = _sub.get("Name")

                result.append(_instance)
        return result

    @property
    def security_groups(self) -> list[dict]:
        """Return a list of EC2 security groups."""
        result: list[dict] = []
        for i in self.client.describe_security_groups()["SecurityGroups"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def security_group_rules(self) -> list[dict]:
        """Return a list of EC2 security group rules."""
        result: list[dict] = []
        for i in self.client.describe_security_group_rules()["SecurityGroupRules"]:
            _rules: dict = {
                "session": self.session.profile_name,
                "GroupName": None,
                **i,
            }
            for group in self.security_groups:
                if group.get("GroupId") == i.get("GroupId"):
                    _rules["GroupName"] = group.get("GroupName")
                    break
                result.append(_rules)
        return result

    @property
    def vpcs(self) -> list[dict]:
        """Return a list of EC2 VPCs."""
        result: list[dict] = []
        for i in self.client.describe_vpcs()["Vpcs"]:
            _vpc: dict = {"session": self.session.profile_name, "VpcName": None, **i}
            for tag in i.get("Tags", []):
                if tag.get("Key") == "Name":
                    _vpc["VpcName"] = tag.get("Value")
                    break
            result.append(_vpc)
        return result

    @property
    def subnets(self) -> list[dict]:
        """Return a list of EC2 subnets."""
        result: list[dict] = []
        for i in self.client.describe_subnets()["Subnets"]:
            _subnet: dict = {
                "session": self.session.profile_name,
                "SubnetName": None,
                "VpcName": None,
                **i,
            }

            for _vps in self.vpcs:
                if _vps.get("VpcId") == i.get("VpcId"):
                    _subnet["VpcName"] = _vps.get("VpcName")
                    break

            for tag in i.get("Tags", []):
                if tag.get("Key") == "Name":
                    _subnet["SubnetName"] = tag.get("Value")
                    break

            result.append({"session": self.session.profile_name, **i})

        return result

    @property
    def internet_gateways(self) -> list[dict]:
        """Return a list of EC2 internet gateways."""
        result: list[dict] = []
        for i in self.client.describe_internet_gateways()["InternetGateways"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def route_tables(self) -> list[dict]:
        """Return a list of EC2 route tables."""
        result: list[dict] = []
        for i in self.client.describe_route_tables()["RouteTables"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def network_acls(self) -> list[dict]:
        """Return a list of EC2 network ACLs."""
        result: list[dict] = []
        for i in self.client.describe_network_acls()["NetworkAcls"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def network_interfaces(self) -> list[dict]:
        """Return a list of EC2 network interfaces."""
        result: list[dict] = []
        for i in self.client.describe_network_interfaces()["NetworkInterfaces"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def volumes(self) -> list[dict]:
        """Return a list of EC2 volumes."""
        result: list[dict] = []
        for i in self.client.describe_volumes()["Volumes"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def snapshots(self) -> list[dict]:
        """Return a list of EC2 snapshots."""
        result: list[dict] = []
        for i in self.client.describe_snapshots(OwnerIds=["self"])["Snapshots"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def images(self) -> list[dict]:
        """Return a list of EC2 images."""
        result: list[dict] = []
        for i in self.client.describe_images(Owners=["self"])["Images"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> dict[str, list[dict]]:
        """Return a dictionary of the service instance data.

        Args:
        ----
            filtered (bool, optional): Whether to filter the data. Defaults to True.

        Returns:
        -------
            dict[str, list[dict]]: The service instance data
        """
        if not filtered:
            return {
                "Instances": self.instances,
                "SecurityGroups": self.security_groups,
                "SecurityGroupRules": self.security_group_rules,
                "Vpcs": self.vpcs,
                "Subnets": self.subnets,
                "InternetGateways": self.internet_gateways,
                "RouteTables": self.route_tables,
                "NetworkAcls": self.network_acls,
                "NetworkInterfaces": self.network_interfaces,
                "Volumes": self.volumes,
                "Snapshots": self.snapshots,
                "Images": self.images,
            }

        return {
            "Instances": filter_and_sort_dict_list(
                self.instances,
                [
                    "session",
                    "InstanceId",
                    "Name",
                    "SSMManaged",
                    "State",
                    "KeyName",
                    "PrivateIpAddress",
                    "PublicIpAddress",
                    "VpcName",
                    "SubnetName",
                    "SecurityGroups",
                    "Tags",
                    "InstanceType",
                    "ImageId",
                    "LaunchTime",
                ],
            ),
            "SecurityGroups": filter_and_sort_dict_list(
                self.security_groups,
                [
                    "session",
                    "GroupId",
                    "GroupName",
                    "Description",
                    "Tags",
                ],
            ),
            "SecurityGroupRules": filter_and_sort_dict_list(
                self.security_group_rules,
                [
                    "session",
                    "SecurityGroupRuleId",
                    "IsEgress",
                    "IpProtocol",
                    "FromPort",
                    "ToPort",
                    "CidrIpv4",
                    "CidrIpv6",
                    "PrefixlistId",
                    "ReferencedGroupInfo",
                    "SecurityGroupName",
                    "Description",
                ],
            ),
            "Vpcs": filter_and_sort_dict_list(
                self.vpcs,
                [
                    "session",
                    "VpcId",
                    "VpcName",
                    "CidrBlock",
                    "IsDefault",
                    "State",
                    "CidrBlockAssociationSet",
                    "InstanceTenancy",
                    "Tags",
                ],
            ),
            "Subnets": filter_and_sort_dict_list(
                self.subnets,
                [
                    "session",
                    "VpcId",
                    "VpcName",
                    "SubnetName",
                    "AvailabilityZone",
                    "SubnetId",
                    "CidrBlock",
                    "AvailableIpAddressCount",
                    "MapPublicIpOnLaunch",
                    "State",
                    "DefaultForAz",
                    "Tags",
                ],
            ),
            "InternetGateways": filter_and_sort_dict_list(
                self.internet_gateways,
                [
                    "session",
                    "InternetGatewayId",
                    "Attachments",
                    "Tags",
                ],
            ),
            "RouteTables": filter_and_sort_dict_list(
                self.route_tables,
                [
                    "session",
                    "VpcId",
                    "RouteTableId",
                    "Routes",
                    "Associations",
                    "Tags",
                ],
            ),
            "NetworkAcls": filter_and_sort_dict_list(
                self.network_acls,
                [
                    "session",
                    "NetworkAclId",
                    "VpcId",
                    "IsDefault",
                    "Entries",
                    "Associations",
                    "Tags",
                ],
            ),
            "NetworkInterfaces": filter_and_sort_dict_list(
                self.network_interfaces,
                [
                    "session",
                    "NetworkInterfaceId",
                    "PrivateIpAddress",
                    "InterfaceType",
                    "AvailabilityZone",
                    "SubnetId",
                    "Description",
                    "VpcId",
                    "Groups",
                    "Ipv6Addresses",
                    "MacAddress",
                    "OwnerId",
                    "PrivateIpAddresses",
                    "Status",
                    "Attachment",
                    "Tags",
                ],
            ),
            "Volumes": filter_and_sort_dict_list(
                self.volumes,
                [
                    "session",
                    "VolumeId",
                    "AvailabilityZone",
                    "VolumeType",
                    "Encrypted",
                    "Size",
                    "State",
                    "SnapshotId",
                    "Tags",
                    "CreateTime",
                    "Attachments",
                ],
            ),
            "Snapshots": filter_and_sort_dict_list(
                self.snapshots,
                [
                    "session",
                    "SnapshotId",
                    "State",
                    "Progress",
                    "VolumeId",
                    "VolumeSize",
                    "Description",
                    "Encrypted",
                    "StartTime",
                    "Tags",
                ],
            ),
            "Images": filter_and_sort_dict_list(
                self.images,
                [
                    "session",
                    "Architecture",
                    "Description",
                    "ImageType",
                    "EnaSupport",
                    "Platform",
                    "Public",
                    "RootDeviceType",
                    "CreationDate",
                    "Hypervisor",
                    "ImageId",
                    "ImageLocation",
                    "KernelId",
                    "Name",
                    "OwnerId",
                    "RamdiskId",
                    "RootDeviceName",
                    "SriovNetSupport",
                    "State",
                    "Tags",
                    "VirtualizationType",
                ],
            ),
        }
