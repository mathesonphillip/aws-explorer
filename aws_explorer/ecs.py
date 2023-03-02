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
            self._logger.debug(
                f"{self._session.profile_name:<20} clusters (not cached)"
            )
            response = self.client.list_clusters()
            self._clusters = response.get("clusterArns")
            return self._clusters

        self._logger.debug(f"{self._session.profile_name:<20} clusters (cached)")
        return self._clusters

    @property
    def services(self):
        if not self._services:
            self._logger.debug(
                f"{self._session.profile_name:<20} services (not cached)"
            )
            response = self.client.list_services()
            self._services = response.get("serviceArns")
            return self._services

        self._logger.debug(f"{self._session.profile_name:<20} services (cached)")
        return self._services

    @property
    def task_definitions(self):
        if not self._task_definitions:
            self._logger.debug(
                f"{self._session.profile_name:<20} task_definitions (not cached)"
            )
            response = self.client.list_task_definitions()
            self._task_definitions = response.get("taskDefinitionArns")
            return self._task_definitions

        self._logger.debug(
            f"{self._session.profile_name:<20} task_definitions (cached)"
        )
        return self._task_definitions

    def to_dict(self):
        """This method is used to convert the object to Dict."""

        data = {
            "Clusters": self.clusters,
            "Services": self.services,
            "TaskDefinitions": self.task_definitions,
        }

        return data
