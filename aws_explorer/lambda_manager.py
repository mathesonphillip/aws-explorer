import logging


class LambdaManager:
    def __init__(self, session):
        self.logger = logging.getLogger(__name__)
        self.session = session
        self.client = self.session.client("lambda")
        self._functions = None
