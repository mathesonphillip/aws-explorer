from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class S3Manager:
    """This class is used to manage S3 resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("s3")

    @property
    def buckets(self) -> List[Dict]:
        result: List = []
        for i in self.client.list_buckets()["Buckets"]:
            _bucket: Dict = {"Account": self.session.profile_name, **i}
            if b_name := i.get("Name"):
                _bucket["Location"] = self.client.get_bucket_location(Bucket=b_name).get("LocationConstraint")
                _bucket["Encryption"] = self.client.get_bucket_encryption(Bucket=b_name)
            result.append(_bucket)
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
        if not filtered:
            return {"Buckets": self.buckets}

        return {
            "Buckets": filter_and_sort_dict_list(
                self.buckets,
                [
                    "Account",
                    "Name",
                    "Location",
                    "Encryption",
                    "CreationDate",
                ],
            )
        }
