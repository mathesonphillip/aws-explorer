from .utils import filter_and_sort_dict_list


class CloudWatchManager:
    def __init__(self, session):
        self._session = session
        self.client = self._session.client("cloudwatch")
        self._alarms = None
        self._metrics = None
        self._alarm_history = None

    @property
    def alarms(self):
        if not self._alarms:
            response = self.client.describe_alarms().get("MetricAlarms")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._alarms = response
            return self._alarms
        return self._alarms

    @property
    def metrics(self):
        if not self._metrics:
            response = self.client.list_metrics().get("Metrics")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._metrics = response
            return self._metrics
        return self._metrics

    @property
    def alarm_history(self):
        response = self.client.describe_alarm_history(
            MaxRecords=100, HistoryItemType="StateUpdate", ScanBy="TimestampDescending"
        ).get("AlarmHistoryItems")
        _ = [item.update({"Account": self._session.profile_name}) for item in response]
        self._alarm_history = response

        return self._alarm_history

    def to_dict(self, filtered=True):
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
                    # "AlarmArn",
                    # "Statistic",
                    # "Dimensions",
                    # "Period",
                    # "EvaluationPeriods",
                    "Threshold",
                    "ComparisonOperator",
                    # "TreatMissingData",
                    # "EvaluateLowSampleCountPercentile",
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
