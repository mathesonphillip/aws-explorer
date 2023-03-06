"""Class module for the DynamoDBManager class, which is used to interact with the AWS DynamoDB service."""


import boto3

from .utils import filter_and_sort_dict_list


class DynamoDBManager:

    """This class is used to manage DynamoDB resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("dynamodb")

    @property
    def table_name(self) -> list[dict]:
        """Return a list of DynamoDB table names."""
        result: list[dict] = []
        for i in self.client.list_tables()["TableNames"]:
            result.append({"session": self.session.profile_name, "TableName": i})
        return result

    @property
    def tables(self) -> list[dict]:
        """Return a list of DynamoDB tables."""
        result: list[dict] = []
        for i in self.table_name:
            t = self.client.describe_table(TableName=i["TableName"])
            result.append({"session": self.session.profile_name, **t})
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
            return {"tables": self.tables}
        return {
            "tables": filter_and_sort_dict_list(
                self.tables,
                [
                    "session",
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
