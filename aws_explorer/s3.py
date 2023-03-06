""" Class module for the S3Manager class, which is used to interact with the AWS S3 service. """


from functools import cached_property
import boto3


class S3Manager:

    """This class is used to manage S3 resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("s3")

    @cached_property
    def buckets(self) -> list[dict]:
        """Return a list of S3 buckets."""
        result: list = []

        return result

    def __repr__(self) -> str:
        return f"<S3Manager session={self.session.profile_name}>"

    # def to_dict(self, filtered: bool = True) -> dict[str, list[dict]]:
    #     """Return a dictionary of the service instance data

    #     Args:
    #         filtered (bool, optional): Whether to filter the data. Defaults to True.

    #     Returns:
    #         dict[str, list[dict]]: The service instance data
    #     """
    #     if not filtered:
    #         return {"Buckets": self.buckets}

    #     return {
    #         "Buckets": filter_and_sort_dict_list(
    #             self.buckets,
    #             [
    #                 "session",
    #                 "Name",
    #                 "Location",
    #                 "Encryption",
    #                 "CreationDate",
    #             ],
    #         )
    #     }
