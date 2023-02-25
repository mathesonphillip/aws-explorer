#!/usr/bin/env python
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
import logging

import boto3

# from .logger import get_logger

# logger = get_logger(__name__)
# logger.info("Starting program...")

# ---------------------------------------------------------------------------- #
#                                   S3Manager                                  #
# ---------------------------------------------------------------------------- #


class S3Manager:
    """This class is used to manage S3 resources."""

    def __init__(self, session):
        # self.logger = logging.getLogger(__name__)
        # logging.basicConfig(level=logging.DEBUG,
        #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # self.logger.debug("Phil")
        # # logger.info("Creating S3Manager...")

        self.session = session
        self.s3 = self.session.client("s3")
        self._buckets = None

        print(self.s3.list_buckets())

    @property
    def buckets(self):
        """This property is used to get a list of S3 buckets."""
        if not self._buckets:
            response = self.s3.list_buckets()["Buckets"]
            print(response)
            self._buckets = response
        return self._buckets

    def to_dict(self):
        """This method is used to convert the object to Dict."""
        return self.__dict__

    def __repr__(self):
        repr_str = ""
        for key, val in self.__dict__.items():
            if key == "s3":
                continue

            repr_str += f"{key}: {val}, "

        return f"S3Manager({repr_str[:-2]})"


# ---------------------------------------------------------------------------- #
#                                  EC2Manager                                  #
# ---------------------------------------------------------------------------- #


class EC2Manager:
    """This class is used to manage EC2 resources."""

    def __init__(self, session):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger.debug("Phil")

        self.session = session
        self.ec2 = session.client("ec2")
        self._instances = list

    @property
    def instances(self):
        """This property is used to get a list of EC2 instances."""
        if not self._instances:
            instances = self.ec2.describe_instances()["Reservations"]
            for instance in instances:
                instance = instance.get("Instances")
                if not instance:
                    break
                self._instances.append(instance[0])

        return self._instances

    def to_dict(self):
        """This method is used to convert the object to Dict."""
        return self.__dict__

    def __repr__(self):
        repr_str = ""
        for key, val in self.__dict__.items():
            if key == "ec2":
                continue

            repr_str += f"{key}: {val}, "

        return f"EC2Manager({repr_str[:-2]})"


# ---------------------------------------------------------------------------- #
#                                  STSManager                                  #
# ---------------------------------------------------------------------------- #


class STSManager:
    """This class is used to manage STS resources."""

    def __init__(self, session):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger.debug("Phil")
        print(f">   STS Manager: {session}")
        # logger.info("Creating STSManager...")

        self.session = session
        self.sts = self.session.client("sts")
        self._identity = None

    @property
    def identity(self):
        """This property is used to get the identity of the caller."""
        if not self._identity:
            response = self.sts.get_caller_identity()
            del response["ResponseMetadata"]
            self._identity = response
        return self._identity

    def to_dict(self):
        """This method is used to convert the object to Dict."""
        return self.__dict__

    def __repr__(self):
        repr_str = ""
        for key, val in self.__dict__.items():
            if key == "sts":
                continue

            repr_str += f"{key}: {val}, "

        # print(f"<   STS Manager:")
        return f"STSManager({repr_str[:-2]})"


# ---------------------------------------------------------------------------- #
#                                  IAMManager                                  #
# ---------------------------------------------------------------------------- #
# iam
# users
# alias


class IAMManager:
    """This class is used to manage IAM resources."""

    def __init__(self, session):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger.debug("Phil")
        # logger.info("Creating IAMManager...")
        self.session = session
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

    def to_dict(self):
        """This method is used to convert the object to Dict."""
        return self.__dict__

    def __repr__(self):
        repr_str = ""
        for key, val in self.__dict__.items():
            if key == "iam":
                continue

            repr_str += f"{key}: {val}, "

        return f"IAMManager({repr_str[:-2]})"


# ---------------------------------------------------------------------------- #
#                                    Account                                   #
# ---------------------------------------------------------------------------- #


class Account:
    """This class is used to manage AWS accounts."""

    def __init__(self, profile_name=None):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger.debug("Phil")
        # Set logger level
        # self.logger.setLevel(logging.DEBUG)

        self.logger.debug(f">   Account:init:profile_name={profile_name}")

        # logger.info("Creating Account...")

        self.profile = profile_name

        self.session = boto3.Session(profile_name=profile_name)
        self.logger.debug(f"    Account:init:session={self.session}")

        self.sts = STSManager(self.session)

        identity = self.sts.identity
        self.id = identity.get("Account")
        self.user = identity.get("UserId")

        self.iam = IAMManager(self.session)
        self.alias = self.name = self.iam.alias

        self.s3 = S3Manager(self.session)
        self.ec2 = EC2Manager(self.session)

    def to_dict(self):
        """This method is used to convert the object to Dict."""
        return self.__dict__

    def __repr__(self):
        response = {
            "id": self.id,
            "user": self.user,
            "name": self.name,
            "alias": self.alias,
        }

        response = json.dumps(response)
        self.logger.debug("<   Account:repr")
        self.logger.debug("Phil")
        return response


# ---------------------------------------------------------------------------- #
