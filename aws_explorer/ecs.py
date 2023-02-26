import logging


class ECSManager:
    def __init__(self, session):
        self.logger = logging.getLogger(__name__)
        self.session = session
        self.client = self.session.client("ecs")
        self.containers = None
        self.containers2 = None
