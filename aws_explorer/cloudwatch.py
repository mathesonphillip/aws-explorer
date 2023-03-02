from .utils import get_logger


class CloudWatchManager:
    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} cloudwatch.__init__()")
        self._session = session
        self.client = self._session.client("cloudwatch")
        self._alarms = None
        self._metrics = None

    @property
    def alarms(self):
        if not self._alarms:
            self._logger.debug(f"{self._session.profile_name:<20} alarms (not cached)")
            response = self.client.describe_alarms().get("MetricAlarms")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._alarms = response
            return self._alarms
        self._logger.debug(f"{self._session.profile_name:<20} alarms (cached)")
        return self._alarms

    @property
    def metrics(self):
        if not self._metrics:
            self._logger.debug(f"{self._session.profile_name:<20} metrics (not cached)")
            response = self.client.list_metrics().get("Metrics")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._metrics = response
            return self._metrics
        self._logger.debug(f"{self._session.profile_name:<20} metrics (cached)")
        return self._metrics

    def to_dict(self):
        """This method is used to convert the object to Dict."""

        return {"Alarms": self.alarms, "Metrics": self.metrics}
