""" Class module for the CloudWatchManager class, which is used to interact with the AWS CloudWatch service. """


import boto3

from .utils import filter_and_sort_dict_list


class CloudWatchManager:

    """This class is used to manage CloudWatch resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("cloudwatch")

    @property
    def alarms(self) -> list[dict]:
        """Return a list of CloudWatch alarms."""
        result: list[dict] = []
        for i in self.client.describe_alarms()["MetricAlarms"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def metrics(self) -> list[dict]:
        """Return a list of CloudWatch metrics."""
        result: list[dict] = []
        for i in self.client.list_metrics()["Metrics"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def alarm_history(self) -> list[dict]:
        """Return a list of CloudWatch alarm history."""
        result: list[dict] = []
        for i in self.client.describe_alarm_history()["AlarmHistoryItems"]:
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
                "Alarms": self.alarms,
                "Metrics": self.metrics,
                "AlarmHistory": self.alarm_history,
            }

        return {
            "Alarms": filter_and_sort_dict_list(
                self.alarms,
                [
                    "session",
                    "AlarmName",
                    "AlarmDescription",
                    "Namespace",
                    "MetricName",
                    "StateValue",
                    "StateReason",
                    "StateUpdatedTimestamp",
                    "Threshold",
                    "ComparisonOperator",
                ],
            ),
            "Metrics": filter_and_sort_dict_list(
                self.metrics,
                [
                    "session",
                    "Namespace",
                    "MetricName",
                    "Dimensions",
                ],
            ),
            "AlarmHistory": self.alarm_history,
        }
