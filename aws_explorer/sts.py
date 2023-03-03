from typing import Dict

import boto3


class STSManager:
    """This class is used to manage STS resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("sts")

    @property
    def get_identity(self) -> object:
        return self.client.get_caller_identity()

    def to_dict(self, filtered: bool = True) -> Dict[str, object]:
        if not filtered:
            return {"Identity": self.get_identity}

        return {"Identity": self.get_identity}
