""" Class module for the SSMManager class, which is used to interact with the AWS SSM service. """


import boto3

from .utils import filter_and_sort_dict_list


class SSMManager:

    """This class is used to manage SSM resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("ssm")

    @property
    def parameters(self) -> list[dict]:
        """Return a list of SSM parameters."""
        result: list[dict] = []
        for i in self.client.describe_parameters()["Parameters"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    # @property
    # def instances(self) -> list[dict]:
    #     """Return a list of SSM instances."""
    #     result: list[dict] = []
    #     for i in self.client.describe_instance_information()["InstanceInformationlist"]:
    #         result.append({"session": self.session.profile_name, **i})
    #     return result

    # def run_command(self, instance_ids, document_name, parameters, comment):  # pylint: disable=unused-argument
    #     """Run a command on an instance."""

    # def to_dict(self, filtered: bool = True) -> dict[str, list[dict]]:
    #     """Return a dictionary of the service instance data.

    #     Args:
    #     ----
    #         filtered (bool, optional): Whether to filter the data. Defaults to True.

    #     Returns:
    #     -------
    #         dict[str, list[dict]]: The service instance data
    #     """
    #     if not filtered:
    #         return {"Parameters": self.parameters, "Instances": self.instances}

    #     return {
    #         "Parameters": filter_and_sort_dict_list(self.parameters, ["session", "Name", "Type", "LastModifiedDate"]),
    #         "Instances": filter_and_sort_dict_list(
    #             self.instances,
    #             [
    #                 "session",
    #                 "ComputerName",
    #                 "InstanceId",
    #                 "PingStatus",
    #                 "LastPingDateTime",
    #                 "AgentVersion",
    #                 "IsLatestVersion",
    #                 "ResourceType",
    #                 "IPAddress",
    #                 "PlatformType",
    #                 "PlatformName",
    #                 "PlatformVersion",
    #             ],
    #         ),
    #     }
