"""Class module for the EC2Manager class, which is used to interact with the AWS EC2 service."""


from .types import Instance, SecurityGroup, SecurityGroupRule, InstanceSecurityGroupRule, InstanceTag, InstanceSecurityGroup
from functools import cached_property


class EC2Manager:

    """This class is used to manage EC2 resources."""

    def __init__(self, session) -> None:
        # self.session = session._session
        # self.client = self.session.client("sts")

        self.parent = session
        self.client = self.parent._session.client("ec2")
        self._resources: list[str] = [
            "instances",
            "instance_tags",
            "instance_security_groups",
            "instance_security_group_rules",
            "security_groups",
            "security_group_rules",
        ]

    @cached_property
    def instances(self) -> list[Instance]:
        """Return a list of EC2 instances."""
        instances: list[Instance] = []
        for res in self.client.describe_instances()["Reservations"]:
            for instance in res.get("Instances", []):
                # Create an Instance object

                i = Instance.parse_obj(instance)
                # Add the account id and name to the instance object
                # i.AccountId = self.session.client("sts").get_caller_identity()["Account"]
                # i.AccountName = self.session.client("iam").list_account_aliases()["AccountAliases"][0]

                # TODO: Refac and move thses to own functions
                # Add the instance name to the object (if it exists)
                i.Name = [tag.get("Value") for tag in i.Tags if tag.get("Key") == "Name"][0]

                # Get a list of all the ssm managed instances and check if the current instance is in it (set limit)
                # TODO: Fix this calling wronte session, need to get ssm client from parent session
                ssm_instances = self.parent._session.client("ssm").describe_instance_information(MaxResults=50).get("InstanceInformationList", [])

                # Loop through the list of ssm managed instances and check if the current instance is in it, if so return true
                i.SSMManaged = any([True for ssm_instance in ssm_instances if ssm_instance.get("InstanceId") == i.InstanceId])

                # Get a list of all VPCs and check if the current instance is in it
                # If it is, add the VPC name to the instance object
                vpcs = self.client.describe_vpcs()["Vpcs"]
                i.VpcName = [vpc.get("Tags", [{}])[0].get("Value") for vpc in vpcs if vpc.get("VpcId") == i.VpcId][0]

                # Get a list of all subnets and check if the current instance is in it
                # If it is, add the subnet name to the instance object
                subnets = self.client.describe_subnets()["Subnets"]
                i.SubnetName = [subnet.get("Tags", [{}])[0].get("Value") for subnet in subnets if subnet.get("SubnetId") == i.SubnetId][0]

                instances.append(i)
        return instances

    @cached_property
    def security_groups(self) -> list[SecurityGroup]:
        """Return a list of EC2 security groups."""
        security_groups: list[SecurityGroup] = []
        for security_group in self.client.describe_security_groups()["SecurityGroups"]:
            group = SecurityGroup.parse_obj(security_group)

            # Add the account id and name to the instance object
            group.AccountId = self.parent.sts.identity.account_id
            group.AccountName = self.parent.sts.identity.alias

            for instance in self.instances:
                for sg in instance.SecurityGroups:
                    if group.GroupId == sg.get("GroupId"):
                        group.Instances.append((instance.Name, instance.InstanceId))

            security_groups.append(group)

        return security_groups

    @cached_property
    def security_group_rules(self) -> list[SecurityGroupRule]:
        """Return a list of EC2 security group rules."""
        security_group_rules: list[SecurityGroupRule] = []
        for security_group_rule in self.client.describe_security_group_rules()["SecurityGroupRules"]:
            security_group_rule = SecurityGroupRule.parse_obj(security_group_rule)

            # Add the account id and name to the instance object
            security_group_rule.AccountId = self.parent.sts.identity.account_id
            security_group_rule.AccountName = self.parent.sts.identity.alias

            for security_group in self.security_groups:
                if security_group.GroupId == security_group_rule.GroupId:
                    security_group_rule.GroupName = security_group.GroupName
                    security_group_rule.Instances = security_group.Instances
                    break

            security_group_rules.append(SecurityGroupRule.parse_obj(security_group_rule))

        return security_group_rules

    @cached_property
    def instance_security_groups(self) -> list[InstanceSecurityGroup]:
        """Return a list of EC2 security group rules."""
        instance_security_groups: list[InstanceSecurityGroup] = []
        for instance in self.instances:
            for group in instance.SecurityGroups:
                instance_security_group = InstanceSecurityGroup(
                    AccountId=self.parent.sts.identity.account_id,
                    AccountName=self.parent.sts.identity.alias,
                    InstanceId=instance.InstanceId,
                    InstanceName=instance.Name,
                    GroupId=group.get("GroupId"),
                    GroupName=group.get("GroupName"),
                )
                instance_security_groups.append(instance_security_group)
        return instance_security_groups

    @cached_property
    def instance_tags(self) -> list[InstanceTag]:
        """Return a list of EC2 instance tags."""
        instance_tags: list[InstanceTag] = []
        for instance in self.instances:
            for tag in instance.Tags:
                instance_tag = InstanceTag(
                    AccountId=self.parent.sts.identity.account_id,
                    AccountName=self.parent.sts.identity.alias,
                    InstanceId=instance.InstanceId,
                    InstanceName=instance.Name,
                    Key=tag.get("Key"),
                    Value=tag.get("Value"),
                )
                instance_tags.append(instance_tag)
        return instance_tags

    @cached_property
    def instance_security_group_rules(self) -> list[InstanceSecurityGroupRule]:
        """Return a list of EC2 security group rules."""

        instance_security_rules: list[InstanceSecurityGroupRule] = []
        for instance in self.instances:
            for security_group in instance.SecurityGroups:
                for security_group_rule in self.security_group_rules:
                    if security_group_rule.GroupId == security_group.get("GroupId"):
                        rule = InstanceSecurityGroupRule(
                            AccountId=self.parent.sts.identity.account_id,
                            AccountName=self.parent.sts.identity.alias,
                            InstanceId=instance.InstanceId,
                            InstanceName=instance.Name,
                            IsEgress=security_group_rule.IsEgress,
                            IpProtocol=security_group_rule.IpProtocol,
                            FromPort=security_group_rule.FromPort,
                            ToPort=security_group_rule.ToPort,
                            CidrIpv4=security_group_rule.CidrIpv4,
                            CidrIpv6=security_group_rule.CidrIpv6,
                            PrefixListId=security_group_rule.PrefixListId,
                            GroupName=security_group.get("GroupName"),
                            GroupId=security_group.get("GroupId"),
                        )
                        instance_security_rules.append(rule)

        return instance_security_rules

    @cached_property
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

    @cached_property
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

    @cached_property
    def internet_gateways(self) -> list[dict]:
        """Return a list of EC2 internet gateways."""
        result: list[dict] = []
        for i in self.client.describe_internet_gateways()["InternetGateways"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @cached_property
    def route_tables(self) -> list[dict]:
        """Return a list of EC2 route tables."""
        result: list[dict] = []
        for i in self.client.describe_route_tables()["RouteTables"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @cached_property
    def network_acls(self) -> list[dict]:
        """Return a list of EC2 network ACLs."""
        result: list[dict] = []
        for i in self.client.describe_network_acls()["NetworkAcls"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @cached_property
    def network_interfaces(self) -> list[dict]:
        """Return a list of EC2 network interfaces."""
        result: list[dict] = []
        for i in self.client.describe_network_interfaces()["NetworkInterfaces"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @cached_property
    def volumes(self) -> list[dict]:
        """Return a list of EC2 volumes."""
        result: list[dict] = []
        for i in self.client.describe_volumes()["Volumes"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @cached_property
    def snapshots(self) -> list[dict]:
        """Return a list of EC2 snapshots."""
        result: list[dict] = []
        for i in self.client.describe_snapshots(OwnerIds=["self"])["Snapshots"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @cached_property
    def images(self) -> list[dict]:
        """Return a list of EC2 images."""
        result: list[dict] = []
        for i in self.client.describe_images(Owners=["self"])["Images"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    # @cached_property
    def export(self) -> dict:
        print("Exporting EC2 resources")

        export_data = {}
        for resource_type in self._resources:
            print(f"Exporting {resource_type}...")
            export_data[resource_type] = []
            for i in resource_type:
                resource_data = getattr(self, resource_type)
                for resource in resource_data:
                    export_data[resource_type].append(resource.dict(exclude_none=True))
        return export_data
