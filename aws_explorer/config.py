from .utils import get_logger


class CloudTrailManager:
    """This class is used to manage CloudTrail resources."""

    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} cloudtrail.__init__()")
        self._session = session
        self.cloudtrail = self._session.client("cloudtrail")
        self._trails = None

    @property
    def trails(self):
        """This property is used to get a list of CloudTrail trails."""
        if not self._trails:
            self._logger.debug(f"{self._session.profile_name:<20} trails (!cached)")
            response = self.cloudtrail.describe_trails().get("trailList")
            self._trails = response
        self._logger.debug(f"{self._session.profile_name:<20} trails (cached)")
        return self._trails

    @property
    def trail_names(self):
        """This property is used to get a list of CloudTrail trail names."""
        return [trail.get("Name") for trail in self.trails]

    def get_trail(self, trail_name):
        """This method is used to get a CloudTrail trail."""
        return self.cloudtrail.get_trail(Name=trail_name)

    def get_trail_status(self, trail_name):
        """This method is used to get the status of a CloudTrail trail."""
        return self.cloudtrail.get_trail_status(Name=trail_name)

    def get_trail_events(self, trail_name, start_time, end_time):
        """This method is used to get events from a CloudTrail trail."""
        return self.cloudtrail.lookup_events(
            LookupAttributes=[
                {"AttributeKey": "EventId", "AttributeValue": trail_name}
            ],
            StartTime=start_time,
            EndTime=end_time,
        )

    def to_dict(self):
        """This method is used to convert a CloudTrail manager to a dictionary."""
        return {
            "trails": self.trails,
            "trail_names": self.trail_names,
        }


class ConfigManager:
    """This class is used to manage configuration files."""

    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} config.__init__()")
        self._session = session
        self.config = self._session.client("config")
        self._rules = None

    @property
    def rules(self):
        """This property is used to get a list of Config rules."""
        if not self._rules:
            self._logger.debug(f"{self._session.profile_name:<20} rules (!cached)")
            response = self.config.describe_config_rules().get("ConfigRules")
            self._rules = response
        self._logger.debug(f"{self._session.profile_name:<20} rules (cached)")
        return self._rules

    def to_dict(self):
        """This method is used to convert a Config manager to a dictionary."""
        return {
            "rules": self.rules,
        }
