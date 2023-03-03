""" This module contains the Account class and its related classes.
    The Account class is the main class of the aws_explorer package.
    It is used to create an object that represents an AWS account.
"""

import json
from datetime import datetime
from typing import Any, Callable, Dict, Iterator, List, Optional

import boto3
import pandas as pd
import yaml
from deepmerge import always_merger  # type: ignore

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
from .rds import RDSManager
from .s3 import S3Manager
from .ssm import SSMManager
from .sts import STSManager
from .utils import remove_timezones_from_object


class Account:
    """This class is used to manage AWS accounts."""

    def __init__(self, profile: str, region: str) -> None:
        if not profile or not region:
            raise ValueError("profile and region are required")

        self.session: boto3.Session = boto3.Session(
            profile_name=profile, region_name=region
        )
        self._initialise_services()

    # ---------------------------------------------------------------------------- #

    def _initialise_services(self) -> None:
        """This method is used to initialise the service managers."""
        self.backup = BackupManager(self.session)
        self.cloudformation = CloudFormationManager(self.session)
        self.cloudtrail = CloudTrailManager(self.session)
        self.cloudwatch = CloudWatchManager(self.session)
        self.cloudwatch_logs = CloudWatchLogsManager(self.session)
        self.config = ConfigManager(self.session)
        self.dynamo_db = DynamoDBManager(self.session)
        self.ec2 = EC2Manager(self.session)
        self.ecs = ECSManager(self.session)
        self.iam = IAMManager(self.session)
        self.lamb = LambdaManager(self.session)
        self.rds = RDSManager(self.session)
        self.s3 = S3Manager(self.session)
        self.ssm = SSMManager(self.session)
        self.sts = STSManager(self.session)

    # ---------------------------------------------------------------------------- #

    def to_dict(self, filtered: bool = True) -> Dict[str, object]:
        """Return object as dict"""

        return {
            # "SSM": self.ssm.to_dict(filtered=filtered),
            # "EC2": self.ec2.to_dict(filtered=filtered),
            # "IAM": self.iam.to_dict(filtered=filtered),
            # "S3": self.s3.to_dict(filtered=filtered),
            # "CloudWatchLogs": self.cloudwatch_logs.to_dict(filtered=filtered),
            # "CloudWatch": self.cloudwatch.to_dict(filtered=filtered),
            # "Backup": self.backup.to_dict(filtered=filtered),
            # "CloudFormation": self.cloudformation.to_dict(filtered=filtered),
            # "Config": self.config.to_dict(filtered=filtered),
            "DynamoDB": self.dynamo_db.to_dict(filtered=filtered),
            # "ECS": self.ecs.to_dict(filtered=filtered),
            "Lambda": self.lamb.to_dict(filtered=filtered),
            "RDS": self.rds.to_dict(filtered=filtered),
            "CloudTrail": self.cloudtrail.to_dict(filtered=filtered),
        }

    # ---------------------------------------------------------------------------- #

    def to_json(self, indent: int = 4) -> str:
        """Return object as JSON"""
        return json.dumps(self.to_dict(), default=str, indent=indent)

    # ---------------------------------------------------------------------------- #
    def export_to_json(self, obj: Any, export_path: str) -> None:
        with open(export_path, "w", encoding="utf8") as file:
            file.write(json.dumps(obj))

    def export_to_yaml(self, obj: Any, export_path: str) -> None:
        with open(export_path, "w", encoding="utf8") as file:
            yaml.dump(obj, file)

    def export_to_excel(self, obj: Any, export_path: str) -> None:
        # Get the data as a dictionary

        data_dict = remove_timezones_from_object(obj)

        # pylint: disable=abstract-class-instantiated
        with pd.ExcelWriter(path=export_path) as writer:
            # iterate over the top-level keys in the dictionary
            for service_key in data_dict:  # type: ignore
                for key, data in data_dict[service_key].items():  # type: ignore
                    sheet_name = f"{service_key}.{key}"

                    print(f"Writing {sheet_name} to Excel")

                    df = pd.DataFrame(data)
                    df.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        startrow=1,
                        header=False,
                        index=False,
                    )

                    column_settings: List[Dict[str, str]] = [
                        {"header": column} for column in df.columns
                    ]

                    # Add the Excel table structure. Pandas will add the data.
                    worksheet = writer.sheets[sheet_name]
                    worksheet.add_table(
                        0,
                        0,
                        len(df),
                        len(df.columns) - 1,
                        {"name": sheet_name, "columns": column_settings},
                    )

                    # Set the column width to the max length of the column header
                    # for column in df:
                    #     column_length = max(df[column].astype(str).map(len).max(), len(column))
                    #     col_idx = df.columns.get_loc(column)
                    #     writer.sheets[sheet_name].set_column(col_idx, col_idx, column_length)

    def get_filename(self, extension: str) -> str:
        """This function is used to get the filename."""
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"{self.session.profile_name}_{timestamp}.{extension}"

    def export(self, extension: str, export_path: str = ".") -> None:
        """This method is used to export the account to a file."""
        # Define a dictionary with file extensions and corresponding file writing functions
        file_writers = {
            "json": self.export_to_json,
            "yaml": self.export_to_yaml,
            "xlsx": self.export_to_excel,
        }

        # Get the file writing function corresponding to the file extension
        file_writer: Optional[Callable[[Any, str], None]] = file_writers.get(extension)

        if file_writer is None:
            raise ValueError(f"Unsupported file extension: {extension}")

        # Get the filename and full export path
        filename = self.get_filename(extension)
        full_export_path = f"{export_path}/{filename}"

        # Call the file writing function with the object and export path
        file_writer(self.to_dict(), full_export_path)

    # ---------------------------------------------------------------------------- #
    def __repr__(self) -> str:
        """Return object as string"""
        return f"Account({self.session.profile_name})"


# ---------------------------------------------------------------------------- #
