from mypy_boto3_rds import RDSClient

from .utils import filter_and_sort_dict_list, get_logger


class RDSManager:
    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} rds.__init__()")
        self._session = session
        self.client: RDSClient = self._session.client("rds")
        self._instances = None
        self._clusters = None

    @property
    def instances(self):
        if not self._instances:
            self._logger.debug(
                f"{self._session.profile_name:<20} instances (not cached)"
            )
            response = self.client.describe_db_instances().get("DBInstances")

            # Add Account to each item
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._instances = response

            return self._instances

        self._logger.debug(f"{self._session.profile_name:<20} instances (cached)")
        return self._instances

    @property
    def clusters(self):
        if not self._clusters:
            self._logger.debug(
                f"{self._session.profile_name:<20} clusters (not cached)"
            )
            response = self.client.describe_db_clusters().get("DBClusters")

            # Add Account to each item
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._clusters = response

            return self._clusters

        self._logger.debug(f"{self._session.profile_name:<20} clusters (cached)")
        return self._clusters

    def to_dict(self, filtered=True):
        if not filtered:
            return {
                "Instances": self.instances,
                "Clusters": self.clusters,
            }

        return {
            "Instances": filter_and_sort_dict_list(
                self.instances,
                [
                    "Account",
                    "DBInstanceIdentifier",
                    "DBInstanceClass",
                    "Engine",
                    "EngineVersion",
                    "DBInstanceStatus",
                    "MasterUsername",
                    "Endpoint",
                    "AllocatedStorage",
                    "DBInstanceArn",
                ],
            ),
            "Clusters": filter_and_sort_dict_list(
                self.clusters,
                [
                    "Account",
                    "DBClusterIdentifier",
                    "Engine",
                    "EngineVersion",
                    "DBClusterStatus",
                    "MasterUsername",
                    "Endpoint",
                    "AllocatedStorage",
                    "DBClusterArn",
                ],
            ),
        }
