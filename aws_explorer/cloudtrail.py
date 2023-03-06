"""Class module for the CloudTrailManager class, which is used to interact with the AWS CloudTrail service."""


import boto3

from .utils import filter_and_sort_dict_list


class CloudTrailManager:

    """This class is used to manage CloudTrail resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("cloudtrail")

    @property
    def trails(self) -> list[dict]:
        """Return a list of CloudTrail trails."""
        result: list[dict] = []
        for i in self.client.describe_trails()["traillist"]:
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
                "trails": self.trails,
            }
        return {
            "trails": filter_and_sort_dict_list(
                self.trails,
                [
                    "session",
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
