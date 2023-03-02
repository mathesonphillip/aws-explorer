from .utils import get_logger


class ECSManager:
    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} ecs.__init__()")
        self._session = session
        self.client = self._session.client("ecs")
        self.containers = None
        self.containers2 = None
