""" This module contains the Account class and its related classes.
    The Account class is the main class of the aws_explorer package.
    It is used to create an object that represents an AWS account.
    The Account class contains the following properties:
        - s3: An S3Manager object
        - ec2: An EC2Manager object
        - sts: An STSManager object
        - iam: An IAMManager object
"""

import json

import boto3 as b3

from .logger import get_logger

logger = get_logger(__name__)
logger.info("Starting program...")

# ---------------------------------------------------------------------------- #
#                                   S3Manager                                  #
# ---------------------------------------------------------------------------- #


class S3Manager:
    """This class is used to manage S3 resources."""

    def __init__(self, session: b3.Session):
        logger.info("Creating S3Manager...")
        self.s3 = session.client("s3")
        self._buckets = None

    @property
    def buckets(self):
        """This property is used to get a list of S3 buckets."""
        if not self._buckets:
            response = self.s3.list_buckets()["Buckets"]
            self._buckets = response
        return self._buckets

    def to_json(self):
        """This method is used to convert the S3Manager object to JSON."""
        return json.dumps(self.__dict__, default=str)

    def __repr__(self):
        return self.to_json()


# ---------------------------------------------------------------------------- #
#                                  EC2Manager                                  #
# ---------------------------------------------------------------------------- #


class EC2Manager:
    """This class is used to manage EC2 resources."""

    def __init__(self, session: b3.Session):
        logger.info("Creating EC2Manager...")
        self.ec2 = session.client("ec2")
        self._instances: list[object] = []

    @property
    def instances(self) -> list[object]:
        """This property is used to get a list of EC2 instances."""
        if not self._instances:
            instances = self.ec2.describe_instances()["Reservations"]
            for instance in instances:
                instance = instance.get("Instances")
                if not instance:
                    break
                self._instances.append(instance[0])

        return self._instances

    def to_json(self):
        """This method is used to convert the EC2Manager object to JSON."""
        return json.dumps(self.__dict__, default=str)

    def __repr__(self):
        return self.to_json()


# ---------------------------------------------------------------------------- #
#                                  STSManager                                  #
# ---------------------------------------------------------------------------- #


class STSManager:
    """This class is used to manage STS resources."""

    def __init__(self, session: b3.Session):
        logger.info("Creating STSManager...")
        self.sts = session.client("sts")
        self._identity = None

    @property
    def identity(self):
        """This property is used to get the identity of the caller."""
        if not self._identity:
            response = self.sts.get_caller_identity()
            self._identity = response
        return self._identity

    def to_json(self):
        """This method is used to convert the STSManager object to JSON."""
        return json.dumps(self.__dict__, default=str)

    def __repr__(self):
        return self.to_json()


# ---------------------------------------------------------------------------- #
#                                  IAMManager                                  #
# ---------------------------------------------------------------------------- #


class IAMManager:
    """This class is used to manage IAM resources."""

    def __init__(self, session: b3.Session):
        logger.info("Creating IAMManager...")
        self.iam = session.client("iam")
        self._users = None
        self._alias = None

    @property
    def users(self):
        """This property is used to get a list of IAM users."""
        if not self._users:
            response = self.iam.list_users().get("Users")
            self._users = response
        return self._users

    @property
    def alias(self):
        """This property is used to get the alias of the account."""
        if not self._alias:
            response = self.iam.list_account_aliases().get("AccountAliases")
            if response:
                self._alias = response[0]
        return self._alias

    def to_json(self):
        """This method is used to convert the IAMManager object to JSON."""
        return json.dumps(self.__dict__, default=str)

    def __repr__(self):
        return self.to_json()


# ---------------------------------------------------------------------------- #
#                                    Account                                   #
# ---------------------------------------------------------------------------- #


class Account:
    """This class is used to manage AWS accounts."""

    def __init__(self, profile_name: str | None = None):
        logger.info("Creating Account...")

        self.profile = profile_name
        self.session = b3.Session(profile_name=profile_name)

        self.sts = STSManager(self.session)
        identity = self.sts.identity
        self.id = identity.get("Account")
        self.user = identity.get("UserId")

        self.iam = IAMManager(self.session)
        self.alias = self.name = self.iam.alias

        self.s3 = S3Manager(self.session)
        self.ec2 = EC2Manager(self.session)

    def to_json(self):
        """This method is used to convert the Account object to JSON."""
        return self.__dict__

    def __repr__(self):
        response = {
            "id": self.id,
            "user": self.user,
            "name": self.name,
            "alias": self.alias,
        }

        response = json.dumps(response)
        return response


# ---------------------------------------------------------------------------- #
