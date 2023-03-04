"""Class module for the STSManager class, which is used to interact with the AWS STS service."""


from typing import Dict

import boto3


class STSManager:
    """This class is used to manage STS resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("sts")

    @property
    def get_identity(self) -> object:
        """Return the identity of the caller. Good for confirming the everything is working."""
        return self.client.get_caller_identity()

    def to_dict(self, filtered: bool = True) -> Dict[str, object]:
        """Return a dictionary of the service instance data

        Args:
            filtered (bool, optional): Whether to filter the data. Defaults to True.

        Returns:
            Dict[str, List[Dict]]: The service instance data
        """
        if not filtered:
            return {"Identity": self.get_identity}

        return {"Identity": self.get_identity}
