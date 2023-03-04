""" Class module for the LambdaManager class, which is used to interact with the AWS Lambda service. """

from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class LambdaManager:
    """This class is used to manage Lambda resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("lambda")

    @property
    def functions(self) -> List[Dict]:
        """Return a list of Lambda functions"""
        result: List = []
        for i in self.client.list_functions()["Functions"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
        """Return a dictionary of the service instance data

        Args:
            filtered (bool, optional): Whether to filter the data. Defaults to True.

        Returns:
            Dict[str, List[Dict]]: The service instance data
        """
        if not filtered:
            return {"Functions": self.functions}

        return {
            "Functions": filter_and_sort_dict_list(
                self.functions,
                [
                    "Account",
                    "FunctionName",
                    "Description",
                    "Runtime",
                    "Timeout",
                    "MemorySize",
                    "CodeSize",
                    "LastModified",
                    "Environment",
                    "Handler",
                    "Role",
                    "FunctionArn",
                ],
            )
        }
