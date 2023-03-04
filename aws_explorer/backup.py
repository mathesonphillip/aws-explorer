"""Class module for the BackupManager class, which is used to interact with the AWS Backup service."""


from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class BackupManager:
    """This class is used to manage Backup resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("backup")

    @property
    def vaults(self) -> List[Dict]:
        """Return a list of Backup vaults"""
        result: List[Dict] = []
        for i in self.client.list_backup_vaults()["BackupVaultList"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def plans(self) -> List[Dict]:
        """Return a list of Backup plans"""
        result: List[Dict] = []
        for i in self.client.list_backup_plans()["BackupPlansList"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def jobs(self) -> List[Dict]:
        """Return a list of Backup jobs"""
        result: List[Dict] = []
        for i in self.client.list_backup_jobs()["BackupJobs"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
        """Return a dictionary of the service instance data

        Args:
            filtered (bool, optional): Whether to filter the data. Defaults to True.

        Returns:
            Dict[str, List[Dict]]: The service instance data
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
                    "Account",
                    "BackupVaultName",
                    "NumberOfRecoveryPoints",
                    "BackupVaultArn",
                    "EncryptionKeyArn",
                ],
            ),
            "Plans": filter_and_sort_dict_list(
                self.plans,
                [
                    "Account",
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
                    "Account",
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
