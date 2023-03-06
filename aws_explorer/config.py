""" Class module for the ConfigManager class, which is used to interact with the AWS Config service. """


import boto3

from .utils import filter_and_sort_dict_list


class ConfigManager:

    """This class is used to manage configuration files."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.config = self.session.client("config")

    @property
    def rules(self) -> list[dict]:
        """Return a list of Config rules."""
        result: list[dict] = []
        for i in self.config.describe_config_rules()["ConfigRules"]:
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
                "rules": self.rules,
            }
        return {
            "rules": filter_and_sort_dict_list(
                self.rules,
                [
                    "session",
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
