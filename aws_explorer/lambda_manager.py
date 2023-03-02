from .utils import get_logger


class LambdaManager:
    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} lambda.__init__()")
        self._session = session
        self.client = self._session.client("lambda")
        self._functions = None
