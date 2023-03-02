from .utils import get_logger


class ECSManager:
    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} ecs.__init__()")
        self._session = session
        self.client = self._session.client("ecs")
        self._clusters = None
        self._services = None
        self._task_definitions = None

    @property
    def clusters(self):
        if not self._clusters:
            response = self.client.list_clusters().get("clusterArns")
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._clusters = response

        return self._clusters

    @property
    def services(self):
        if not self._services:
            response = self.client.list_services().get("serviceArns")
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._services = response

        return self._services

    @property
    def task_definitions(self):
        if not self._task_definitions:
            response = self.client.list_task_definitions().get("taskDefinitionArns")
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._task_definitions = response

        return self._task_definitions

    def to_dict(self):
        """This method is used to convert the object to Dict."""

        data = {
            "Clusters": self.clusters,
            "Services": self.services,
            "TaskDefinitions": self.task_definitions,
        }

        return data
