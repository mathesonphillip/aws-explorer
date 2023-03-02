from .utils import get_logger


class CloudFormationManager:
    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} cloudformation.__init__()")

        self._session = session
        self.client = self._session.client("cloudformation")

        self._stacks = None

    def to_dict(self):
        """Return object as dict"""
        return self.__dict__
