"""Class module for the ECSManager class, which is used to interact with the AWS ECS service."""


import boto3

from .utils import filter_and_sort_dict_list


class ECSManager:

    """This class is used to manage ECS resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("ecs")

    @property
    def clusters(self) -> list[dict]:
        """Return a list of ECS clusters."""
        result: list = []
        for i in self.client.describe_clusters()["clusters"]:
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
            return {
                "Clusters": self.clusters,
            }

        return {
            "Clusters": filter_and_sort_dict_list(
                self.clusters,
                [
                    "createdAt",
                    "registeredAt",
                    "updatedAt",
                ],
            ),
        }
