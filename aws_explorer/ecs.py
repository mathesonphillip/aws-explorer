from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class ECSManager:
    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("ecs")

    @property
    def clusters(self) -> List[Dict]:
        result: List = []
        for i in self.client.describe_clusters()["clusters"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
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
