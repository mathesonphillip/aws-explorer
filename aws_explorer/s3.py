import logging


class S3Manager:
    """This class is used to manage S3 resources."""

    def __init__(self, session):
        self.logger = logging.getLogger(__name__)
        self.session = session
        self.s3 = self.session.client("s3")
        self._buckets = None

    @property
    def buckets(self):
        """This property is used to get a list of S3 buckets."""

        if not self._buckets:
            response = self.s3.list_buckets()["Buckets"]
            print(response)
            self._buckets = response
        return self._buckets

    def to_dict(self):
        """This method is used to convert the object to Dict."""
        return self.__dict__
