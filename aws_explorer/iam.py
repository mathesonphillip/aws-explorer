import logging


class IAMManager:
    """This class is used to manage IAM resources."""

    def __init__(self, session):
        self.logger = logging.getLogger(__name__)
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
