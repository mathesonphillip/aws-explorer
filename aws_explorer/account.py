""" This module contains the Account class and its related classes.
    The Account class is the main class of the aws_explorer package.
    It is used to create an object that represents an AWS account.
"""

import json
import logging

import boto3

from .backup import BackupManager
from .cloudformation import CloudFormationManager
from .ec2 import EC2Manager
from .ecs import ECSManager
from .iam import IAMManager
from .lambda_manager import LambdaManager
from .s3 import S3Manager
from .sts import STSManager


class Account:
    """This class is used to manage AWS accounts."""

    def __init__(self, profile_name=None):
        self.logger = logging.getLogger(__name__)
        self.session = boto3.Session(profile_name=profile_name)
        self._initialise_services()

        # identity = self.sts.identity
        # self.id = identity.get("Account")
        # self.user = identity.get("UserId")
        # self.alias = self.name = self.iam.alias

    def _initialise_services(self):
        self.sts = STSManager(self.session)
        self.iam = IAMManager(self.session)
        self.s3 = S3Manager(self.session)
        self.ec2 = EC2Manager(self.session)
        self.cf = CloudFormationManager(self.session)
        self.backup = BackupManager(self.session)
        self.lamb = LambdaManager(self.session)
        self.ecs = ECSManager(self.session)

    def to_dict(self):
        """Return object as dict"""
        return self.__dict__
