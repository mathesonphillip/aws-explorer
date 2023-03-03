from .utils import get_logger


class STSManager:
    """This class is used to manage STS resources."""

    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} sts.__init__()")
        self._session = session
        self.client = self._session.client("sts")
        self._identity = None

    @property
    def identity(self):
        """This property is used to get the identity of the caller."""
        if not self._identity:
            self._logger.debug(
                f"{self._session.profile_name:<20} identity (not cached)"
            )
            response = self.client.get_caller_identity()
            del response["ResponseMetadata"]
            self._identity = response
            return self._identity

        self._logger.debug(f"{self._session.profile_name:<20} identity (cached)")
        return self._identity

    def to_dict(self) -> dict[str, dict]:
        """This method is used to convert the object to Dict."""
        data = {
            "Identity": self.identity,
        }

        return data
