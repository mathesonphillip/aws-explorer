""" Class module for the CloudWatchLogsManager class, which is used to interact with the AWS CloudWatchLogs service. """


import boto3

from .utils import filter_and_sort_dict_list


class CloudWatchLogsManager:

    """This class is used to manage CloudWatchLogs resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("logs")

    @property
    def log_groups(self) -> list[dict]:
        """Return a list of cloudwatch log groups and their properties."""
        result: list[dict] = []
        for i in self.client.describe_log_groups()["logGroups"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    # def query_vpc_flow_logs(self, log_group, start_time, end_time):
    #     """
    #     Execute a CloudWatch Insights query #WIP

    #     This is an example of how to execute a CloudWatch Insights query.
    #     NOTE: Need to flesh this workflow out
    #     """
    #     raise NotImplementedError

    #     # create the CloudWatch Insights query
    #     query = "fields @timestamp, @message " "| sort @timestamp desc"

    #     print(f"Query: {query}")

    #     # execute the query
    #     response = self.client.start_query(
    #         logGroupName=log_group,
    #         startTime=int(start_time.timestamp()),
    #         endTime=int(end_time.timestamp()),
    #         queryString=query,
    #         limit=50,
    #     )

    #     # get the query ID and wait for the query to complete
    #     query_id = response["queryId"]
    #     status = None

    #     while status == None or status == "Running" or status == "Scheduled":
    #         status = self.client.get_query_results(queryId=query_id)["status"]
    #         print(f"Query status: {status}")
    #         time.sleep(1)

    #     # get the query results
    #     results = []
    #     query_result = self.client.get_query_results(queryId=query_id)
    #     # print(f"Query results: {query_result}")

    #     format_string = "%Y-%m-%d %H:%M:%S.%f"
    #     for result in query_result["results"]:
    #         timestamp = result[0]["value"]
    #         dt_obj = datetime.strptime(timestamp, format_string)
    #         message = result[1]["value"]

    #         results.append({"timestamp": dt_obj, "message": message})

    #     import pandas as pd

    #     df = pd.DataFrame(results).to_excel("test.xlsx")

    #     return results

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
                "LogGroups": self.log_groups,
            }

        return {
            "LogGroups": filter_and_sort_dict_list(
                self.log_groups,
                [
                    "session",
                    "logGroupName",
                    "storedBytes",
                    "retentionInDays",
                ],
            )
        }
