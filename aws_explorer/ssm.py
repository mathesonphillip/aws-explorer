from .utils import get_logger


class SSMManager:
    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} ssm.__init__()")
        self._session = session
        self.client = self._session.client("ssm")
        self._parameters = None
        self._instances = None

    @property
    def parameters(self):
        if not self._parameters:
            self._logger.debug(
                f"{self._session.profile_name:<20} parameters (not cached)"
            )
            response = self.client.describe_parameters()
            self._parameters = response.get("Parameters")
            return self._parameters

        self._logger.debug(f"{self._session.profile_name:<20} parameters (cached)")
        return self._parameters

    @property
    def instances(self):
        if not self._instances:
            self._logger.debug(
                f"{self._session.profile_name:<20} instances (not cached)"
            )
            response = self.client.describe_instance_information()
            self._instances = response.get("InstanceInformationList")
            return self._instances

        self._logger.debug(f"{self._session.profile_name:<20} instances (cached)")
        return self._instances

    def to_dict(self):
        """This method is used to convert the object to Dict."""

        data = {"Parameters": self.parameters, "Instances": self.instances}

        return data
