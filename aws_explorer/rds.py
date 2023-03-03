from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class RDSManager:
    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("rds")

    @property
    def instances(self) -> List[object]:
        result: List = []
        for i in self.client.describe_db_instances()["DBInstances"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def clusters(self) -> List[object]:
        result: List = []
        for i in self.client.describe_db_clusters()["DBClusters"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[object]]:
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
