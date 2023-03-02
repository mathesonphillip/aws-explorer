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

    def to_dict(self):
        """This method is used to convert a CloudTrail manager to a dictionary."""
        return {
            "trails": self.trails,
        }
