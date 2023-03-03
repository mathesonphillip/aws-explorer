from .utils import filter_and_sort_dict_list, get_logger


class CloudWatchLogsManager:
    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} cloudwatch_logs.__init__()")
        self._session = session
        self.client = self._session.client("logs")
        self._log_groups = None

    @property
    def log_groups(self):
        if not self._log_groups:
            self._logger.debug(
                f"{self._session.profile_name:<20} log_groups (not cached)"
            )
            response = self.client.describe_log_groups().get("logGroups")

            # Add Account to each item
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._log_groups = response
            return self._log_groups
        self._logger.debug(f"{self._session.profile_name:<20} log_groups (cached)")
        return self._log_groups

    def to_dict(self, filtered=True):
        if not filtered:
            return {
                "LogGroups": self.log_groups,
            }

        return {
            "LogGroups": filter_and_sort_dict_list(
                self.log_groups,
                [
                    "Account",
                    "logGroupName",
                    "storedBytes",
                    "retentionInDays",
                    # "metricFilterCount",
                    # "creationTime",
                    # "arn",
                ],
            )
        }
