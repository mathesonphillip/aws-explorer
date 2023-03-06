"""Class module for the BackupManager class, which is used to interact with the AWS Backup service."""


import boto3

from .utils import filter_and_sort_dict_list


class BackupManager:

    """This class is used to manage Backup resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("backup")

    @property
    def vaults(self) -> list[dict]:
        """Return a list of Backup vaults."""
        result: list[dict] = []
        for i in self.client.list_backup_vaults()["BackupVaultlist"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def plans(self) -> list[dict]:
        """Return a list of Backup plans."""
        result: list[dict] = []
        for i in self.client.list_backup_plans()["BackupPlanslist"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    @property
    def jobs(self) -> list[dict]:
        """Return a list of Backup jobs."""
        result: list[dict] = []
        for i in self.client.list_backup_jobs()["BackupJobs"]:
            result.append({"session": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> dict[str, list[dict]]:
        """Return a dictionary of the service instance data.

        Args:
        ----
            filtered (bool, optional): Whether to filter the data. Defaults to True.

        Returns:
        -------
            dict[str, list[dict]]: The service instance data
        """
        if not filtered:
            return {
                "Vaults": self.vaults,
                "Plans": self.plans,
                "Jobs": self.jobs,
            }

        return {
            "Vaults": filter_and_sort_dict_list(
                self.vaults,
                [
                    "session",
                    "BackupVaultName",
                    "NumberOfRecoveryPoints",
                    "BackupVaultArn",
                    "EncryptionKeyArn",
                ],
            ),
            "Plans": filter_and_sort_dict_list(
                self.plans,
                [
                    "session",
                    "BackupPlanName",
                    "LastExecutionDate",
                    "CreationDate",
                    "BackupPlanId",
                    "BackupPlanArn",
                ],
            ),
            "Jobs": filter_and_sort_dict_list(
                self.jobs,
                [
                    "session",
                    "BackupVaultName",
                    "State",
                    "PercentDone",
                    "StartBy",
                    "CreationDate",
                    "CompletionDate",
                    "BackupSizeInBytes",
                    "ResourceType",
                    "CreatedBy",
                    "ResourceArn",
                    "BackupJobId",
                    "BackupVaultArn",
                    "RecoveryPointArn",
                ],
            ),
        }
