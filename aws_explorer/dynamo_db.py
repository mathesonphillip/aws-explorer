from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class DynamoDBManager:
    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("dynamodb")

    @property
    def table_name(self) -> List[Dict]:
        result: List[Dict] = []
        for i in self.client.list_tables()["TableNames"]:
            result.append(
                {"Account": self.session.profile_name, "TableName": i})
        return result

    @property
    def tables(self) -> List[Dict]:
        result: List[Dict] = []
        for i in self.table_name:
            t = self.client.describe_table(TableName=i["TableName"])
            result.append({"Account": self.session.profile_name, **t})
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
        """This method is used to convert the object to Dict."""
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
