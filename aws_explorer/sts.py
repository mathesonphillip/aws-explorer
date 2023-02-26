import logging


class STSManager:
    """This class is used to manage STS resources."""

    def __init__(self, session):
        self.logger = logging.getLogger(__name__)
        self.session = session
        self.sts = self.session.client("sts")
        self._identity = None

    @property
    def identity(self):
        """This property is used to get the identity of the caller."""
        if not self._identity:
            response = self.sts.get_caller_identity()
            del response["ResponseMetadata"]
            self._identity = response
        return self._identity

    def to_dict(self):
        """This method is used to convert the object to Dict."""
        return self.__dict__
