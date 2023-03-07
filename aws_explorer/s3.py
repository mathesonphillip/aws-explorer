""" Class module for the S3Manager class, which is used to interact with the AWS S3 service. """


from functools import cached_property
from .types import Bucket
from .utils import get_logger


class S3Manager:

    """This class is used to manage S3 resources."""

    def __init__(self, session) -> None:
        self.parent = session
        self.client = self.parent._session.client("s3")
        self._resources: list[str] = [
            "buckets",
        ]

    @cached_property
    def buckets(self) -> list[Bucket]:
        """Return a list of S3 buckets."""
        print("Getting buckets")

        buckets: list[Bucket] = []
        for bucket in self.client.list_buckets()["Buckets"]:
            b = Bucket.parse_obj(bucket)
            b.location = self._get_bucket_location(b.name)
            b.encryption = self._get_bucket_encryption(b.name)

            buckets.append(b)

        return buckets

    def _get_bucket_location(self, bucket_name: str) -> str:
        """Return the location of a bucket."""
        print("Getting bucket location")
        return self.client.get_bucket_location(Bucket=bucket_name)["LocationConstraint"]

    def _get_bucket_encryption(self, bucket_name: str) -> str:
        """Return the encryption of a bucket."""
        print("Getting bucket encryption")

        # Need to call the api as cant seem to access data from the session object
        account_id = self.parent.sts.identity.account_id

        encryption = self.client.get_bucket_encryption(
            Bucket=bucket_name,
            ExpectedBucketOwner=account_id,
        )["ServerSideEncryptionConfiguration"]

        return encryption

    def export(self):
        print("Exporting S3 resources...")
        export_data = {}
        for resource_type in self._resources:
            print(f"Exporting {resource_type}...")

            export_data[resource_type] = []
            for i in resource_type:
                resource_data = getattr(self, resource_type)
                for resource in resource_data:
                    export_data[resource_type].append(resource.dict(exclude_none=True))
        return export_data
