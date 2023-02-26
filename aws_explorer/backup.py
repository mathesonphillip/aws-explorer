import logging


class BackupManager:
    def __init__(self, session):
        self.logger = logging.getLogger(__name__)
        self.session = session
        self.client = self.session.client("backup")
        self.vaults = None
        self.plans = None
        self.jobs = None

    def to_dict(self):
        """Return object as dict"""
        return self.__dict__
