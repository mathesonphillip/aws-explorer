"""Class module for the DynamoDBManager class, which is used to interact with the AWS DynamoDB service."""
from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class DynamoDBManager:
    """This class is used to manage DynamoDB resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("dynamodb")

    @property
    def table_name(self) -> List[Dict]:
        """Return a list of DynamoDB table names"""
        result: List[Dict] = []
        for i in self.client.list_tables()["TableNames"]:
            result.append({"Account": self.session.profile_name, "TableName": i})
        return result

    @property
    def tables(self) -> List[Dict]:
        """Return a list of DynamoDB tables"""
        result: List[Dict] = []
        for i in self.table_name:
            t = self.client.describe_table(TableName=i["TableName"])
            result.append({"Account": self.session.profile_name, **t})
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
        """Return a dictionary of the service instance data

        Args:
            filtered (bool, optional): Whether to filter the data. Defaults to True.

        Returns:
            Dict[str, List[Dict]]: The service instance data
        """
        if not filtered:
            return {"tables": self.tables}
        return {
            "tables": filter_and_sort_dict_list(
                self.tables,
                [
                    "Account",
                    "TableName",
                    "ItemCount",
                    "TableSizeBytes",
                    "TableStatus",
                    "CreationDateTime",
                    "AttributeDefinitions",
                    "BillingModeSummary",
                    "GlobalSecondaryIndexes",
                    "KeySchema",
                    "ProvisionedThroughput",
                    "TableArn",
                    "TableId",
                ],
            )
        }
