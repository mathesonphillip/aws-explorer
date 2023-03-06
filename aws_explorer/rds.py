""" Class module for the RDSManager class, which is used to interact with the AWS RDS service. """


import boto3

from .utils import filter_and_sort_dict_list


class RDSManager:

    """This class is used to manage RDS resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("rds")

    @property
    def instances(self) -> list[object]:
        """Return a list of RDS instances."""
        result: list = []
        for i in self.client.describe_db_instances()["DBInstances"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def clusters(self) -> list[object]:
        """Return a list of RDS clusters."""
        result: list = []
        for i in self.client.describe_db_clusters()["DBClusters"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> dict[str, list[object]]:
        """Return a dictionary of the service instance data.

        Args:
        ----
            filtered (bool, optional): Whether to filter the data. Defaults to True.

        Returns:
        -------
            dict[str, list[object]]: The service instance data
        """

        if not filtered:
            return {
                "Instances": self.instances,
                "Clusters": self.clusters,
            }

        return {
            "Instances": filter_and_sort_dict_list(
                self.instances,
                [
                    "session",
                    "DBInstanceIdentifier",
                    "DBInstanceClass",
                    "Engine",
                    "EngineVersion",
                    "DBInstanceStatus",
                    "MasterUsername",
                    "Endpoint",
                    "AllocatedStorage",
                    "DBInstanceArn",
                ],
            ),
            "Clusters": filter_and_sort_dict_list(
                self.clusters,
                [
                    "session",
                    "DBClusterIdentifier",
                    "Engine",
                    "EngineVersion",
                    "DBClusterStatus",
                    "MasterUsername",
                    "Endpoint",
                    "AllocatedStorage",
                    "DBClusterArn",
                ],
            ),
        }
