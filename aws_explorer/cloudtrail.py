from .utils import filter_and_sort_dict_list


class CloudTrailManager:
    """This class is used to manage CloudTrail resources."""

    def __init__(self, session):
        self._session = session
        self.cloudtrail = self._session.client("cloudtrail")
        self._trails = None

    @property
    def trails(self):
        """This property is used to get a list of CloudTrail trails."""
        if not self._trails:
            response = self.cloudtrail.describe_trails().get("trailList")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._trails = response
        return self._trails

    def to_dict(self, filtered=True):
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
                    # "TrailARN",
                    # "LogFileValidationEnabled",
                    # "CloudWatchLogsLogGroupArn",
                    # "CloudWatchLogsRoleArn",
                ],
            )
        }
