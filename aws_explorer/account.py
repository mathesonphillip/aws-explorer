""" This module contains the Account class and its related classes.
    The Account class is the main class of the aws_explorer package.
    It is used to create an object that represents an AWS account.
"""

import json
from datetime import datetime

import boto3
import pandas as pd
import yaml

from .backup import BackupManager
from .cloudformation import CloudFormationManager
from .cloudtrail import CloudTrailManager
from .cloudwatch import CloudWatchManager
from .cloudwatch_logs import CloudWatchLogsManager
from .config import ConfigManager
from .dynamo_db import DynamoDBManager
from .ec2 import EC2Manager
from .ecs import ECSManager
from .iam import IAMManager
from .lambda_manager import LambdaManager
from .s3 import S3Manager
from .sts import STSManager
from .utils import console, get_logger, remove_timezones_from_dict


class Account:
    """This class is used to manage AWS accounts."""

    _logger = get_logger(__name__)

    def __init__(self, profile=None, region=None):
        self._logger.info(f"{profile:<20} account.__init__()")

        if profile:
            self._logger.debug(
                f"{profile:<20} Creating account from profile: {profile}"
            )
            self.profile = profile
            self.region = region
            self.session = boto3.Session(
                profile_name=self.profile, region_name=self.region
            )

        # Initialise service managers
        self._initialise_services()

    # ---------------------------------------------------------------------------- #

    def _initialise_services(self):
        """This method is used to initialise the service managers."""
        self._logger.debug(f"{self.profile:<20} _initialise_services()")

        self.sts = STSManager(self.session)
        self.iam = IAMManager(self.session)
        self.s3 = S3Manager(self.session)
        self.ec2 = EC2Manager(self.session)
        self.backup = BackupManager(self.session)
        self.lamb = LambdaManager(self.session)
        self.cf = CloudFormationManager(self.session)
        self.dynamo_db = DynamoDBManager(self.session)
        self.ecs = ECSManager(self.session)
        self.cloudwatch = CloudWatchManager(self.session)
        self.cloudwatch_logs = CloudWatchLogsManager(self.session)
        self.cloudtrail = CloudTrailManager(self.session)
        self.config = ConfigManager(self.session)

        # self.id = self.sts.identity.get("Account")
        # self.user_id = self.sts.identity.get("UserId")

    # ---------------------------------------------------------------------------- #

    def to_dict(self, filtered=True):
        """Return object as dict"""
        self._logger.debug(f"{self.profile:<20} to_dict()")
        if not filtered:
            return {
                "IAM": self.iam.to_dict(),
                "S3": self.s3.to_dict(),
                "EC2": self.ec2.to_dict(),
                "Backup": self.backup.to_dict(),
                "Lambda": self.lamb.to_dict(),
                "CloudFormation": self.cf.to_dict(),
                "DynamoDB": self.dynamo_db.to_dict(),
                "CloudWatch": self.cloudwatch.to_dict(),
                "CloudWatchLogs": self.cloudwatch_logs.to_dict(),
                "CloudTrail": self.cloudtrail.to_dict(),
                "Config": self.config.to_dict(),
                # "ECS": self.ecs.to_dict(),
            }

        return {
            "IAM": self.iam.to_dict(filtered=True),
            "S3": self.s3.to_dict(),
            "EC2": self.ec2.to_dict(),
            "Backup": self.backup.to_dict(),
            "Lambda": self.lamb.to_dict(),
            "CloudFormation": self.cf.to_dict(),
            "DynamoDB": self.dynamo_db.to_dict(),
            "CloudWatch": self.cloudwatch.to_dict(),
            "CloudWatchLogs": self.cloudwatch_logs.to_dict(),
            "CloudTrail": self.cloudtrail.to_dict(),
            "Config": self.config.to_dict(),
            # "ECS": self.ecs.to_dict(),
        }

    # ---------------------------------------------------------------------------- #

    def to_json(self, indent=4):
        """Return object as JSON"""
        self._logger.debug(f"{self.profile:<20} to_json()")

        return json.dumps(self.to_dict(), default=str, indent=indent)

    # ---------------------------------------------------------------------------- #

    def export(self, extension, export_path="."):
        """This method is used to export the account to a JSON file."""
        self._logger.debug(f"{self.profile:<20} export()")

        def get_filename(ext):
            """This function is used to get the filename."""
            timestamp = datetime.now().strftime("%Y%m%d")
            return f"{export_path}/{self.profile}_{timestamp}.{ext}"

        if extension == "json":
            with open(get_filename("json"), "w", encoding="utf8") as file:
                file.write(self.to_json())

        if extension == "yaml":
            with open(get_filename("yaml"), "w", encoding="utf8") as file:
                yaml.dump(self.to_dict(), file)

        if extension == "excel":
            # Get the data as a dictionary
            data_dict = remove_timezones_from_dict(self.to_dict())

            # pylint: disable=abstract-class-instantiated
            with pd.ExcelWriter(path=get_filename("xlsx")) as writer:
                # iterate over the top-level keys in the dictionary
                for service_key in data_dict:
                    for key, data in data_dict[service_key].items():  # type: ignore
                        sheet_name = f"{service_key}.{key}"
                        df = pd.DataFrame(data)
                        df.to_excel(
                            writer,
                            sheet_name=sheet_name,
                            startrow=1,
                            header=False,
                            index=False,
                        )

                        column_settings = [{"header": column} for column in df.columns]

                        # Add the Excel table structure. Pandas will add the data.
                        worksheet = writer.sheets[sheet_name]
                        worksheet.add_table(
                            0,
                            0,
                            len(df),
                            len(df.columns) - 1,
                            {"name": sheet_name, "columns": column_settings},
                        )

                        try:
                            worksheet.autofit()
                        except TypeError as e:
                            self._logger.error(e)

        console.print(f"[green]Exported {self.profile} to {export_path}[/green]")

    # ---------------------------------------------------------------------------- #
    def __repr__(self):
        """Return object as string"""
        self._logger.debug("__repr__")

        if self.profile:
            return f"Account({self.profile})"

        # if self.id:
        #     return f"Account({self.id})"

        return "Account()"
