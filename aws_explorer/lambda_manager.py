from .utils import filter_and_sort_dict_list, get_logger


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
            response = self.client.list_functions().get("Functions")
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._functions = response

        return self._functions

    def to_dict(self, filtered=True):
        if not filtered:
            return {"Functions": self.functions}

        return {
            "Functions": filter_and_sort_dict_list(
                self.functions,
                [
                    "Account",
                    "FunctionName",
                    "Description",
                    "Runtime",
                    "Timeout",
                    "MemorySize",
                    "CodeSize",
                    "LastModified",
                    "Environment",
                    "Handler",
                    "Role",
                    "FunctionArn",
                ],
            )
        }
