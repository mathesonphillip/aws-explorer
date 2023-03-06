""" Class module for the CloudFormationManager class, which is used to interact with the AWS CloudFormation service."""


import boto3

from .utils import filter_and_sort_dict_list


class CloudFormationManager:

    """This class is used to manage CloudFormation resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("cloudformation")

    @property
    def stacks(self) -> list[dict]:
        """Return a list of CloudFormation stacks."""
        result: list = []
        for i in self.client.list_stacks()["StackSummaries"]:
            if i["StackStatus"] == "DELETE_COMPLETE":
                continue
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def stack_resources(self) -> list[dict]:
        """Return a list of CloudFormation stack resources."""
        result: list = []
        for stack in self.stacks:
            resources = self.client.list_stack_resources(StackName=stack["StackName"])["StackResourceSummaries"]
            result.extend(resources)
        for i in result:
            i["session"] = self.session.profile_name
        return result

    def detect_drift(self) -> list[str]:
        """This method is used to detect drift in CloudFormation stacks."""
        result: list = []
        for stack in self.stacks:
            drift_id = self.client.detect_stack_drift(StackName=stack["StackName"])["StackDriftDetectionId"]
            result.append(drift_id)
        return result

    def to_dict(self, filtered: bool = True) -> dict[str, list[dict]]:
        """Return a dictionary of the service instance data.

        Args:
        ----
            filtered (bool, optional): Whether to filter the data. Defaults to True.

        Returns:
        -------
            dict[str, list[dict]]: The service instance data
        """
        if not filtered:
            return {
                "Stacks": self.stacks,
                "StackResources": self.stack_resources,
            }

        return {
            "Stacks": filter_and_sort_dict_list(
                self.stacks,
                [
                    "session",
                    "StackName",
                    "StackStatus",
                    "CreationTime",
                    "LastUpdatedTime",
                    "DriftInformation",
                    "TemplateDescription",
                ],
            ),
            "StackResources": filter_and_sort_dict_list(
                self.stack_resources,
                [
                    "session",
                    "StackName",
                    "DriftInformation",
                    "ResourceType",
                    "ResourceStatus",
                    "LogicalResourceId",
                    "PhysicalResourceId",
                    "LastUpdatedTimestamp",
                ],
            ),
        }
