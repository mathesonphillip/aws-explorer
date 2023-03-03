from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class BackupManager:
    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("backup")

    @property
    def vaults(self) -> List[object]:
        result: List = []
        for i in self.client.list_backup_vaults()["BackupVaultList"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def plans(self) -> List[object]:
        result: List = []
        for i in self.client.list_backup_plans()["BackupPlansList"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def jobs(self) -> List[object]:
        result: List = []
        for i in self.client.list_backup_jobs()["BackupJobs"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    def to_dict(self, filtered: bool = True) -> Dict[str, List[object]]:
        """This method is used to convert the object to Dict."""
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
