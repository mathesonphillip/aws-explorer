from .utils import get_logger


class IAMManager:
    """This class is used to manage IAM resources."""

    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} iam.__init__()")
        self._session = session
        self.iam = self._session.client("iam")
        self._users = None
        self._groups = None
        self._roles = None
        self._policies = None
        self._alias = None

    @property
    def users(self):
        """This property is used to get a list of IAM users."""
        if not self._users:
            self._logger.debug(f"{self._session.profile_name:<20} users (!cached)")
            response = self.iam.list_users().get("Users")
            self._users = response

        self._logger.debug(f"{self._session.profile_name:<20} users (cached)")
        return self._users

    @property
    def groups(self):
        """This property is used to get a list of IAM groups."""
        if not self._groups:
            self._logger.debug(f"{self._session.profile_name:<20} groups (!cached)")
            response = self.iam.list_groups().get("Groups")
            self._groups = response
        self._logger.debug(f"{self._session.profile_name:<20} groups (cached)")
        return self._groups

    @property
    def roles(self):
        """This property is used to get a list of IAM roles."""
        if not self._roles:
            self._logger.debug(f"{self._session.profile_name:<20} roles (!cached)")
            response = self.iam.list_roles().get("Roles")
            self._roles = response
        self._logger.debug(f"{self._session.profile_name:<20} roles (cached)")
        return self._roles

    @property
    def policies(self):
        """This property is used to get a list of IAM policies."""
        if not self._policies:
            self._logger.debug(f"{self._session.profile_name:<20} policies (!cached)")
            response = self.iam.list_policies(Scope="Local").get("Policies")
            self._policies = response
        self._logger.debug(f"{self._session.profile_name:<20} policies (cached)")
        return self._policies

    @property
    def alias(self):
        """This property is used to get the alias of the account."""
        if not self._alias:
            self._logger.debug(f"{self._session.profile_name:<20} alias (!cached)")
            response = self.iam.list_account_aliases().get("AccountAliases")
            if response:
                self._alias = response[0]
        self._logger.debug(f"{self._session.profile_name:<20} alias (cached)")
        return self._alias

    def to_dict(self):
        """This method is used to convert the object to Dict."""
        self._logger.debug(f"{self._session.profile_name:<20} to_dict()")
        data = {
            "Users": self.users,
            "Groups": self.groups,
            "Roles": self.roles,
            "Policies": self.policies,
        }

        return data
