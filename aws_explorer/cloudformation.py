import logging


class CloudFormationManager:
    def __init__(self, session):
        self.logger = logging.getLogger(__name__)

        self.session = session
        self.client = self.session.client("cloudformation")

        self._stacks = None

    def to_dict(self):
        """Return object as dict"""
        return self.__dict__
