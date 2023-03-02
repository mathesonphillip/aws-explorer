from .utils import get_logger


class EC2Manager:
    """This class is used to manage EC2 resources."""

    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} ec2.__init__()")
        self._session = session
        self.ec2 = self._session.client("ec2")
        self._instances = list

    @property
    def instances(self):
        """This property is used to get a list of EC2 instances."""
        if not self._instances:
            instances = self.ec2.describe_instances()["Reservations"]
            for instance in instances:
                instance = instance.get("Instances")
                if not instance:
                    break
                self._instances.append(instance[0])

        return self._instances

    def to_dict(self):
        """This method is used to convert the object to Dict."""
        return self.__dict__
