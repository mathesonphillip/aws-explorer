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
            response = self.s3.list_buckets()["Buckets"]
            # print(response)
            self._buckets = response
        return self._buckets

    def to_dict(self):
        """This method is used to convert the object to Dict."""

        data = {"Buckets": self.buckets}

        return data
