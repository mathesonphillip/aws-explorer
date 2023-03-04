""" Class module for the SSMManager class, which is used to interact with the AWS SSM service. """

from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class SSMManager:
    """This class is used to manage SSM resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("ssm")

    @property
    def parameters(self) -> List[Dict]:
        """Return a list of SSM parameters"""
        result: List[Dict] = []
        for i in self.client.describe_parameters()["Parameters"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def instances(self) -> List[Dict]:
        """Return a list of SSM instances"""
        result: List[Dict] = []
        for i in self.client.describe_instance_information()["InstanceInformationList"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    def run_command(
        self, instance_ids, document_name, parameters, comment
    ):  # pylint: disable=unused-argument
        """Run a command on an instance"""

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
        """Return a dictionary of the service instance data

        Args:
            filtered (bool, optional): Whether to filter the data. Defaults to True.

        Returns:
            Dict[str, List[Dict]]: The service instance data
        """
        if not filtered:
            return {"Parameters": self.parameters, "Instances": self.instances}

        return {
            "Parameters": filter_and_sort_dict_list(
                self.parameters, ["Account", "Name", "Type", "LastModifiedDate"]
            ),
            "Instances": filter_and_sort_dict_list(
                self.instances,
                [
                    "Account",
                    "ComputerName",
                    "InstanceId",
                    "PingStatus",
                    "LastPingDateTime",
                    "AgentVersion",
                    "IsLatestVersion",
                    "ResourceType",
                    "IPAddress",
                    "PlatformType",
                    "PlatformName",
                    "PlatformVersion",
                ],
            ),
        }
