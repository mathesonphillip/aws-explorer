""" Class module for the SSMManager class, which is used to interact with the AWS SSM service. """
from .types import SSMInstance

from typing import Callable


class SSMManager:

    """This class is used to manage SSM resources."""

    def __init__(self, session) -> None:
        self.parent = session
        self.client = self.parent._session.client("ssm")
        self._resources: list[str] = [
            "instances"
            # self.parameters,
        ]

    @property
    def parameters(self) -> list[dict]:
        ...

    @property
    def instances(self) -> list[SSMInstance]:
        """Return a list of SSM instances."""
        ssm_instances: list[SSMInstance] = []
        for i in self.client.describe_instance_information()["InstanceInformationList"]:
            instance = SSMInstance(**i)
            instance.AccountId = self.parent.identity.account_id
            instance.AccountName = self.parent.identity.alias
            ssm_instances.append(instance)

        return ssm_instances

    @property
    def resources(self) -> list[Callable]:
        """Return a list of resources."""
        return self._resources

    def run_command(self, instance_ids, document_name, parameters, comment):  # pylint: disable=unused-argument
        ...

    # Define an export method that looks up its current resources and loops through them to export them
    def export(self) -> dict:
        print("Exporting SSM resources")

        export_data = {}
        for resource_type in self.resources:
            export_data[resource_type] = []
            for i in resource_type:
                resource_data = getattr(self, resource_type)
                for resource in resource_data:
                    export_data[resource_type].append(resource.dict(exclude_none=True))
        return export_data
