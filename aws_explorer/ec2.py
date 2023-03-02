from .utils import get_logger


class EC2Manager:
    """This class is used to manage EC2 resources."""

    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} ec2.__init__()")
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

            _ = [
                item.update({"Account": self._session.profile_name}) for item in result
            ]

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
            response = self.ec2.describe_security_group_rules().get(
                "SecurityGroupRules"
            )

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._security_group_rules = response

        return self._security_group_rules

    @property
    def vpcs(self):
        """This property is used to get a list of VPCs."""
        if not self._vpcs:
            response = self.ec2.describe_vpcs().get("Vpcs")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._vpcs = response

        return self._vpcs

    @property
    def subnets(self):
        """This property is used to get a list of subnets."""
        if not self._subnets:
            self._subnets = self.ec2.describe_subnets()["Subnets"]

        return self._subnets

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

    def to_dict(self):
        """This method is used to convert the object to Dict."""

        data = {
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

        return data
