from .utils import filter_and_sort_dict_list


class EC2Manager:
    """This class is used to manage EC2 resources."""

    def __init__(self, session):
        self._session = session
        self.ec2 = self._session.client("ec2")
        self._instances = None
        self._security_groups = None
        self._security_group_rules = None
        self._vpcs = None
        self._subnets = None
        self._internet_gateways = None
        self._route_tables = None
        self._network_acls = None
        self._network_interfaces = None
        self._volumes = None
        self._snapshots = None
        self._images = None

    @property
    def instances(self):
        """This property is used to get a list of EC2 instances."""
        if not self._instances:
            result = []
            instances = self.ec2.describe_instances()["Reservations"]
            for instance in instances:
                instance = instance.get("Instances")
                result.append(instance[0])

            for instance in result:
                instance["Account"] = self._session.profile_name
                instance["Name"] = None
                instance["SSMManaged"] = False
                instance["VpcName"] = False
                instance["SubnetName"] = False

                # Get instance name
                for tag in instance.get("Tags"):
                    if tag.get("Key") == "Name":
                        instance["Name"] = tag.get("Value")

                # Check if instance is an SSM managed instance
                ssm_instances = (
                    self._session.client("ssm")
                    .describe_instance_information()
                    .get("InstanceInformationList")
                )
                for ssm_instance in ssm_instances:
                    if ssm_instance.get("InstanceId") == instance.get("InstanceId"):
                        instance["SSMManaged"] = True

                # Get VPC name
                for vpc in self.vpcs:
                    if vpc.get("VpcId") == instance.get("VpcId"):
                        instance["VpcName"] = vpc.get("Name")
                for subnet in self.subnets:
                    if subnet.get("SubnetId") == instance.get("SubnetId"):
                        instance["SubnetName"] = subnet.get("Name")

            self._instances = result

        return self._instances

    @property
    def security_groups(self):
        """This property is used to get a list of security groups."""
        if not self._security_groups:
            response = self.ec2.describe_security_groups().get("SecurityGroups")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._security_groups = response

        return self._security_groups

    @property
    def security_group_rules(self):
        """This property is used to get a list of security group rules."""
        if not self._security_group_rules:
            rules = self.ec2.describe_security_group_rules().get("SecurityGroupRules")

            groups = self.security_groups

            for rule in rules:
                rule["Account"] = self._session.profile_name
                rule["SecurityGroupName"] = None

                for group in groups:
                    if group.get("GroupId") == rule.get("GroupId"):
                        rule["SecurityGroupName"] = group.get("GroupName")
                        break

            self._security_group_rules = rules

        return self._security_group_rules

    @property
    def vpcs(self):
        """This property is used to get a list of VPCs."""
        vpcs = self.ec2.describe_vpcs().get("Vpcs")
        for vpc in vpcs:
            vpc["Account"] = self._session.profile_name
            vpc["VpcName"] = None

            for tag in vpc.get("Tags"):
                if tag.get("Key") == "Name":
                    vpc["VpcName"] = tag.get("Value")
                    break

        return vpcs

    @property
    def subnets(self):
        """This property is used to get a list of subnets."""
        subnets = self.ec2.describe_subnets()["Subnets"]

        for subnet in subnets:
            subnet["Account"] = self._session.profile_name
            subnet["SubnetName"] = None
            subnet["VpcName"] = None

            for tag in subnet.get("Tags", []):
                if tag.get("Key") == "Name":
                    subnet["Name"] = tag.get("Value")
                    break

            for vpc in self.vpcs:
                if vpc.get("VpcId") == subnet.get("VpcId"):
                    subnet["VpcName"] = vpc.get("Name")
                    break

        return subnets

    @property
    def internet_gateways(self):
        """This property is used to get a list of internet gateways."""
        if not self._internet_gateways:
            response = self.ec2.describe_internet_gateways().get("InternetGateways")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._internet_gateways = response

        return self._internet_gateways

    @property
    def route_tables(self):
        """This property is used to get a list of route tables."""
        if not self._route_tables:
            response = self.ec2.describe_route_tables().get("RouteTables")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._route_tables = response

        return self._route_tables

    @property
    def network_acls(self):
        """This property is used to get a list of network ACLs."""
        if not self._network_acls:
            response = self.ec2.describe_network_acls().get("NetworkAcls")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._network_acls = response

        return self._network_acls

    @property
    def network_interfaces(self):
        """This property is used to get a list of network interfaces."""
        if not self._network_interfaces:
            response = self.ec2.describe_network_interfaces().get("NetworkInterfaces")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._network_interfaces = response

        return self._network_interfaces

    @property
    def volumes(self):
        """This property is used to get a list of volumes."""
        if not self._volumes:
            response = self.ec2.describe_volumes().get("Volumes")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._volumes = response

        return self._volumes

    @property
    def snapshots(self):
        """This property is used to get a list of snapshots."""
        if not self._snapshots:
            response = self.ec2.describe_snapshots(OwnerIds=["self"]).get("Snapshots")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._snapshots = response

        return self._snapshots

    @property
    def images(self):
        """This property is used to get a list of images."""
        if not self._images:
            response = self.ec2.describe_images(Owners=["self"]).get("Images")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._images = response

        return self._images

    def to_dict(self, filtered=True):
        """This method is used to convert the object to Dict."""
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
                    "Account",
                    "InstanceId",
                    "Name",
                    "SSMManaged",
                    "State",
                    "KeyName",
                    "PrivateIpAddress",
                    "PublicIpAddress",
                    "VpcName",
                    "SubnetName",
                    # "VpcId",
                    # "SubnetId",
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
                    "Account",
                    "GroupId",
                    "GroupName",
                    "Description",
                    "Tags",
                ],
            ),
            "SecurityGroupRules": filter_and_sort_dict_list(
                self.security_group_rules,
                [
                    "Account",
                    "SecurityGroupRuleId",
                    "IsEgress",
                    "IpProtocol",
                    "FromPort",
                    "ToPort",
                    "CidrIpv4",
                    "CidrIpv6",
                    "PrefixListId",
                    "ReferencedGroupInfo",
                    "SecurityGroupName",
                    "Description",
                ],
            ),
            "Vpcs": filter_and_sort_dict_list(
                self.vpcs,
                [
                    "Account",
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
                    "Account",
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
                    "Account",
                    "InternetGatewayId",
                    "Attachments",
                    "Tags",
                ],
            ),
            "RouteTables": filter_and_sort_dict_list(
                self.route_tables,
                [
                    "Account",
                    "VpcId",
                    "RouteTableId",
                    "Routes",
                    "Associations",
                    # "PropagatingVgws",
                    "Tags",
                ],
            ),
            "NetworkAcls": filter_and_sort_dict_list(
                self.network_acls,
                [
                    "Account",
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
                    # Add Account Name Lookup
                    "Account",
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
                    # "RequesterId",
                    # "RequesterManaged",
                    # "SourceDestCheck",
                    "Attachment",
                    "Tags",
                ],
            ),
            "Volumes": filter_and_sort_dict_list(
                self.volumes,
                [
                    "Account",
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
                    "Account",
                    "SnapshotId",
                    "State",
                    "Progress",
                    "VolumeId",
                    "VolumeSize",
                    "Description",
                    "Encrypted",
                    # "OwnerId",
                    "StartTime",
                    "Tags",
                ],
            ),
            "Images": filter_and_sort_dict_list(
                self.images,
                [
                    "Account",
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
