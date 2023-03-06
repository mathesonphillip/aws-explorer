""" Class module for the LambdaManager class, which is used to interact with the AWS Lambda service. """


import boto3

from .utils import filter_and_sort_dict_list


class LambdaManager:

    """This class is used to manage Lambda resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("lambda")

    @property
    def functions(self) -> list[dict]:
        """Return a list of Lambda functions."""
        result: list = []
        for i in self.client.list_functions()["Functions"]:
            result.append({"session": self.session.profile_name, **i})
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
            return {"Functions": self.functions}

        return {
            "Functions": filter_and_sort_dict_list(
                self.functions,
                [
                    "session",
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
