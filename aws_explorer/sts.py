"""Class module for the STSManager class, which is used to interact with the AWS STS service."""

import boto3
from functools import cached_property
from .utils import get_logger
from .types import Identity

logger = get_logger(__name__)


class STSManager:

    """This class is used to manage STS resources."""

    def __init__(self, session) -> None:
        print(type(session))

        self.parent = session
        self.client = self.parent._session.client("sts")

    @cached_property
    def identity(self) -> Identity:
        """Return the identity of the caller. Good for confirming the everything is working."""
        identity = Identity.parse_obj(self.client.get_caller_identity())
        # Get the account alias and add it to the identity object, if it exists
        identity.alias = self.parent.iam.alias

        return identity
