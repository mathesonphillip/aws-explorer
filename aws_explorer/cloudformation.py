from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class CloudFormationManager:
    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("cloudformation")

    @property
    def stacks(self) -> List[Dict]:
        result: List = []
        for i in self.client.list_stacks()["StackSummaries"]:
            if i["StackStatus"] == "DELETE_COMPLETE":
                continue
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def stack_resources(self) -> List[Dict]:
        result: List = []
        for stack in self.stacks:
            resources = self.client.list_stack_resources(StackName=stack["StackName"])[
                "StackResourceSummaries"
            ]
            result.extend(resources)
        for i in result:
            i["Account"] = self.session.profile_name
        return result

    def detect_drift(self) -> List[str]:
        """This method is used to detect drift in CloudFormation stacks."""
        result: List = []
        for stack in self.stacks:
            drift_id = self.client.detect_stack_drift(StackName=stack["StackName"])[
                "StackDriftDetectionId"
            ]
            result.append(drift_id)
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
        """This method is used to convert the object to Dict."""
        if not filtered:
            return {
                "Stacks": self.stacks,
                "StackResources": self.stack_resources,
            }

        return {
            "Stacks": filter_and_sort_dict_list(
                self.stacks,
                [
                    "Account",
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
                    "Account",
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
