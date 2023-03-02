from .utils import get_logger


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

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._rules = response
        self._logger.debug(f"{self._session.profile_name:<20} rules (cached)")
        return self._rules

    def to_dict(self):
        """This method is used to convert a Config manager to a dictionary."""
        return {
            "rules": self.rules,
        }
