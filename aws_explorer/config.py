from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class ConfigManager:
    """This class is used to manage configuration files."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.config = self.session.client("config")

    @property
    def rules(self) -> List[Dict]:
        result: List[Dict] = []
        for i in self.config.describe_config_rules()["ConfigRules"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
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
