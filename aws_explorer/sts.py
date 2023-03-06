"""Class module for the STSManager class, which is used to interact with the AWS STS service."""

import boto3
from functools import cached_property
from collections import namedtuple
from .utils import get_logger

STSRepr = namedtuple("STSRepr", ["account_id", "user_id", "arn"])


logger = get_logger(__name__)


class STSManager:

    """This class is used to manage STS resources."""

    def __init__(self, session: boto3.Session) -> None:
        logger.debug(f"Creating STSManager for session {session.profile_name}")

        self.session = session
        self.client = self.session.client("sts")

    @cached_property
    def identity(self) -> object:
        """Return the identity of the caller. Good for confirming the everything is working."""
        response = self.client.get_caller_identity()

        return STSRepr(
            account_id=response["Account"],
            user_id=response["UserId"],
            arn=response["Arn"],
        )

    def __repr__(self) -> str:
        return f"<STSManager session={self.session.profile_name}>"
