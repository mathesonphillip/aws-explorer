from .utils import get_logger


class BackupManager:
    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} backup.__init__()")
        self._session = session
        self.client = self._session.client("backup")
        self._vaults = None
        self._plans = None
        self._jobs = None

    @property
    def vaults(self):
        if not self._vaults:
            self._logger.debug(f"{self._session.profile_name:<20} vaults (not cached)")
            response = self.client.list_backup_vaults().get("BackupVaultList")

            # Add Account to each item
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._vaults = response

            return self._vaults

        self._logger.debug(f"{self._session.profile_name:<20} vaults (cached)")
        return self._vaults

    @property
    def plans(self):
        if not self._plans:
            self._logger.debug(f"{self._session.profile_name:<20} plans (not cached)")
            response = self.client.list_backup_plans().get("BackupPlansList")

            # Add Account to each item
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._plans = response
            return self._plans

        self._logger.debug(f"{self._session.profile_name:<20} plans (cached)")
        return self._plans

    @property
    def jobs(self):
        if not self._jobs:
            self._logger.debug(f"{self._session.profile_name:<20} jobs (not cached)")
            response = self.client.list_backup_jobs().get("BackupJobs")

            # Add Account to each item
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            self._jobs = response

            return self._jobs

        self._logger.debug(f"{self._session.profile_name:<20} jobs (cached)")
        return self._jobs

    def to_dict(self):
        """This method is used to convert the object to Dict."""

        data = {
            "Vaults": self.vaults,
            "Plans": self.plans,
            "Jobs": self.jobs,
        }

        return data
