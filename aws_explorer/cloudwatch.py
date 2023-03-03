from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class CloudWatchManager:
    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("cloudwatch")

    @property
    def alarms(self) -> List[Dict]:
        result: List[Dict] = []
        for i in self.client.describe_alarms()["MetricAlarms"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def metrics(self) -> List[Dict]:
        result: List[Dict] = []
        for i in self.client.list_metrics()["Metrics"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def alarm_history(self) -> List[Dict]:
        result: List[Dict] = []
        for i in self.client.describe_alarm_history()["AlarmHistoryItems"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
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
                    "Account",
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
                    "Account",
                    "Namespace",
                    "MetricName",
                    "Dimensions",
                ],
            ),
            "AlarmHistory": self.alarm_history,
        }
