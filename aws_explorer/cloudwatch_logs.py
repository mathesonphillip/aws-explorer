import time
from datetime import datetime, timedelta

from .utils import filter_and_sort_dict_list


class CloudWatchLogsManager:
    def __init__(self, session):
        self._session = session
        self.client = self._session.client("logs")
        self._log_groups = None

    @property
    def log_groups(self):
        if not self._log_groups:
            response = self.client.describe_log_groups().get("logGroups")

            # Add Account to each item
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._log_groups = response
            return self._log_groups
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
