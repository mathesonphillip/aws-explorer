""" Class module for the RDSManager class, which is used to interact with the AWS RDS service. """

from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class RDSManager:
    """This class is used to manage RDS resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("rds")

    @property
    def instances(self) -> List[object]:
        """Return a list of RDS instances"""
        result: List = []
        for i in self.client.describe_db_instances()["DBInstances"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def clusters(self) -> List[object]:
        """Return a list of RDS clusters"""
        result: List = []
        for i in self.client.describe_db_clusters()["DBClusters"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[object]]:
        """Return a dictionary of the service instance data

        Args:
            filtered (bool, optional): Whether to filter the data. Defaults to True.

        Returns:
            Dict[str, List[object]]: The service instance data
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
                    "Account",
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
                    "Account",
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
