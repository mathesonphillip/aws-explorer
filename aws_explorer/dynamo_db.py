from .utils import filter_and_sort_dict_list


class DynamoDBManager:
    def __init__(self, session):
        self._session = session
        self.client = self._session.client("dynamodb")
        self._tables = None

    @property
    def tables(self):
        if not self._tables:
            table_names = self.client.list_tables().get("TableNames")

            _tables = []
            for table_name in table_names:
                _tables.append(
                    self.client.describe_table(TableName=table_name).get("Table")
                )

            # Add Account to each item
            _ = [
                item.update({"Account": self._session.profile_name}) for item in _tables
            ]

            self._tables = _tables
            return self._tables

        return self._tables

    def to_dict(self, filtered=True):
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
                    # "LatestStreamArn",
                    # "LatestStreamLabel",
                    # "LocalSecondaryIndexes",
                    # "Replicas",
                    # "RestoreSummary",
                    # "SSEDescription",
                    # "StreamSpecification",
                ],
            )
        }
