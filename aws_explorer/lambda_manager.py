from .utils import get_logger


class LambdaManager:
    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} lambda.__init__()")
        self._session = session
        self.client = self._session.client("lambda")
        self._functions = None

    @property
    def functions(self):
        if not self._functions:
            self._logger.debug(
                f"{self._session.profile_name:<20} functions (not cached)"
            )
            response = self.client.list_functions()
            self._functions = response.get("Functions")
            return self._functions

        self._logger.debug(f"{self._session.profile_name:<20} functions (cached)")
        return self._functions

    def to_dict(self):
        """This method is used to convert the object to Dict."""

        data = {"Functions": self.functions}

        return data
