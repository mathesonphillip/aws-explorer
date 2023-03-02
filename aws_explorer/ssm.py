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
            response = self.client.describe_parameters().get("Parameters")
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._parameters = response
        return self._parameters

    @property
    def instances(self):
        if not self._instances:
            response = self.client.describe_instance_information().get(
                "InstanceInformationList"
            )
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._instances = response
        return self._instances

    def to_dict(self):
        """This method is used to convert the object to Dict."""

        data = {"Parameters": self.parameters, "Instances": self.instances}

        return data
