from .utils import filter_and_sort_dict_list


class ConfigManager:
    """This class is used to manage configuration files."""

    def __init__(self, session):
        self._session = session
        self.config = self._session.client("config")
        self._rules = None

    @property
    def rules(self):
        """This property is used to get a list of Config rules."""
        if not self._rules:
            response = self.config.describe_config_rules().get("ConfigRules")

            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._rules = response
        return self._rules

    def to_dict(self, filtered=True):
        """This method is used to convert the object to Dict."""
        if not filtered:
            return {
                "rules": self.rules,
            }
        return {
            "rules": filter_and_sort_dict_list(
                self.rules,
                [
                    "Account",
                    "ConfigRuleName",
                    "Description",
                    "ConfigRuleState",
                    "InputParameters",
                    "Scope",
                    "Source",
                    "Tags",
                    "MaximumExecutionFrequency",
                    "ConfigRuleId",
                    "CreatedBy",
                    "ConfigRuleArn",
                ],
            )
        }
