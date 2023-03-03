from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class CloudTrailManager:
    """This class is used to manage CloudTrail resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("cloudtrail")

    @property
    def trails(self) -> List[Dict]:
        result: List[Dict] = []
        for i in self.client.describe_trails()["trailList"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
        if not filtered:
            return {
                "trails": self.trails,
            }
        return {
            "trails": filter_and_sort_dict_list(
                self.trails,
                [
                    "Account",
                    "Name",
                    "S3BucketName",
                    "S3KeyPrefix",
                    "IsOrganizationTrail",
                    "HomeRegion",
                    "IncludeGlobalServiceEvents",
                    "IsMultiRegionTrail",
                ],
            )
        }
