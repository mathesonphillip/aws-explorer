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
            self._logger.debug(
                f"{self._session.profile_name:<20} instances (not cached)"
            )
            result = []
            instances = self.ec2.describe_instances()["Reservations"]
            for instance in instances:
                instance = instance.get("Instances")
                result.append(instance[0])
            self._instances = result
            return self._instances

        self._logger.debug(f"{self._session.profile_name:<20} instances (cached)")
        return self._instances

    @property
    def security_groups(self):
        """This property is used to get a list of security groups."""
        if not self._security_groups:
            self._logger.debug(
                f"{self._session.profile_name:<20} security_groups (not cached)"
            )
            self._security_groups = self.ec2.describe_security_groups()[
                "SecurityGroups"
            ]

        self._logger.debug(f"{self._session.profile_name:<20} security_groups (cached)")
        return self._security_groups

    @property
    def security_group_rules(self):
        """This property is used to get a list of security group rules."""
        if not self._security_group_rules:
            self._logger.debug(
                f"{self._session.profile_name:<20} security_group_rules (not cached)"
            )
            self._security_group_rules = self.ec2.describe_security_group_rules()[
                "SecurityGroupRules"
            ]

        self._logger.debug(
            f"{self._session.profile_name:<20} security_group_rules (cached)"
        )
        return self._security_group_rules

    @property
    def vpcs(self):
        """This property is used to get a list of VPCs."""
        if not self._vpcs:
            self._logger.debug(f"{self._session.profile_name:<20} vpcs (not cached)")
            self._vpcs = self.ec2.describe_vpcs()["Vpcs"]

        self._logger.debug(f"{self._session.profile_name:<20} vpcs (cached)")
        return self._vpcs

    @property
    def subnets(self):
        """This property is used to get a list of subnets."""
        if not self._subnets:
            self._logger.debug(f"{self._session.profile_name:<20} subnets (not cached)")
            self._subnets = self.ec2.describe_subnets()["Subnets"]

        self._logger.debug(f"{self._session.profile_name:<20} subnets (cached)")
        return self._subnets

    @property
    def internet_gateways(self):
        """This property is used to get a list of internet gateways."""
        if not self._internet_gateways:
            self._logger.debug(
                f"{self._session.profile_name:<20} internet_gateways (not cached)"
            )
            self._internet_gateways = self.ec2.describe_internet_gateways()[
                "InternetGateways"
            ]

        self._logger.debug(
            f"{self._session.profile_name:<20} internet_gateways (cached)"
        )
        return self._internet_gateways

    @property
    def route_tables(self):
        """This property is used to get a list of route tables."""
        if not self._route_tables:
            self._logger.debug(
                f"{self._session.profile_name:<20} route_tables (not cached)"
            )
            self._route_tables = self.ec2.describe_route_tables()["RouteTables"]

        self._logger.debug(f"{self._session.profile_name:<20} route_tables (cached)")
        return self._route_tables

    @property
    def network_acls(self):
        """This property is used to get a list of network ACLs."""
        if not self._network_acls:
            self._logger.debug(
                f"{self._session.profile_name:<20} network_acls (not cached)"
            )
            self._network_acls = self.ec2.describe_network_acls()["NetworkAcls"]

        self._logger.debug(f"{self._session.profile_name:<20} network_acls (cached)")
        return self._network_acls

    @property
    def network_interfaces(self):
        """This property is used to get a list of network interfaces."""
        if not self._network_interfaces:
            self._logger.debug(
                f"{self._session.profile_name:<20} network_interfaces (not cached)"
            )
            self._network_interfaces = self.ec2.describe_network_interfaces()[
                "NetworkInterfaces"
            ]

        self._logger.debug(
            f"{self._session.profile_name:<20} network_interfaces (cached)"
        )
        return self._network_interfaces

    @property
    def volumes(self):
        """This property is used to get a list of volumes."""
        if not self._volumes:
            self._logger.debug(f"{self._session.profile_name:<20} volumes (not cached)")
            self._volumes = self.ec2.describe_volumes()["Volumes"]

        self._logger.debug(f"{self._session.profile_name:<20} volumes (cached)")
        return self._volumes

    @property
    def snapshots(self):
        """This property is used to get a list of snapshots."""
        if not self._snapshots:
            self._logger.debug(
                f"{self._session.profile_name:<20} snapshots (not cached)"
            )
            self._snapshots = self.ec2.describe_snapshots(OwnerIds=["self"])[
                "Snapshots"
            ]

        self._logger.debug(f"{self._session.profile_name:<20} snapshots (cached)")
        return self._snapshots

    @property
    def images(self):
        """This property is used to get a list of images."""
        if not self._images:
            self._logger.debug(f"{self._session.profile_name:<20} images (not cached)")
            self._images = self.ec2.describe_images(Owners=["self"])["Images"]

        self._logger.debug(f"{self._session.profile_name:<20} images (cached)")
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
