""" Class module for the S3Manager class, which is used to interact with the AWS S3 service. """


import boto3

from .utils import filter_and_sort_dict_list


class S3Manager:

    """This class is used to manage S3 resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("s3")

    @property
    def buckets(self) -> list[dict]:
        """Return a list of S3 buckets."""
        result: list = []
        for i in self.client.list_buckets()["Buckets"]:
            _bucket: dict = {"session": self.session.profile_name, **i}
            if b_name := i.get("Name"):
                _bucket["Location"] = self.client.get_bucket_location(Bucket=b_name).get("LocationConstraint")
                _bucket["Encryption"] = self.client.get_bucket_encryption(Bucket=b_name)
            result.append(_bucket)
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
            return {"Buckets": self.buckets}

        return {
            "Buckets": filter_and_sort_dict_list(
                self.buckets,
                [
                    "session",
                    "Name",
                    "Location",
                    "Encryption",
                    "CreationDate",
                ],
            )
        }
