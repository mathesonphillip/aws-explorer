from .utils import get_logger


class S3Manager:
    """This class is used to manage S3 resources."""

    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} s3.__init__()")
        self._session = session
        self.s3 = self._session.client("s3")
        self._buckets = None

    @property
    def buckets(self):
        """This property is used to get a list of S3 buckets."""

        if not self._buckets:
            buckets = self.s3.list_buckets()["Buckets"]
            for bucket in buckets:
                bucket["Location"] = self.s3.get_bucket_location(
                    Bucket=bucket["Name"]
                ).get("LocationConstraint")
                if bucket["Location"] is None:
                    bucket["Location"] = "us-east-1"
                try:
                    bucket["Encryption"] = self.s3.get_bucket_encryption(
                        Bucket=bucket["Name"]
                    ).get("ServerSideEncryptionConfiguration")
                except self.s3.exceptions.ClientError as error:
                    if error.response["Error"]["Code"] == "AccessDenied":
                        bucket["Encryption"] = None
                    else:
                        raise error

            self._buckets = buckets
        return self._buckets

    def to_dict(self):
        """This method is used to convert the object to Dict."""

        data = {"Buckets": self.buckets}

        return data
