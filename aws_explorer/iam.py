from .utils import filter_and_sort_dict_list


class IAMManager:
    """This class is used to manage IAM resources."""

    def __init__(self, session):
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
        users = self.iam.list_users().get("Users", [])

        # mfa_devices = self.iam.list_mfa_devices().get("MFADevices", [])

        for user in users:
            user["Account"] = self._session.profile_name
            user["Groups"] = self.iam.list_groups_for_user(
                UserName=user["UserName"]
            ).get("Groups", [])
            user["Policies"] = self.iam.list_user_policies(
                UserName=user["UserName"]
            ).get("PolicyNames", [])
            user["AttachedPolicies"] = self.iam.list_attached_user_policies(
                UserName=user["UserName"]
            ).get("AttachedPolicies", [])
            user["AccessKeys"] = self.iam.list_access_keys(
                UserName=user["UserName"]
            ).get("AccessKeyMetadata", [])

            # for device in mfa_devices:
            #     if device["UserName"] == user["UserName"]:
            #         user["MFADevices"] = device
            #         break

        return users

    @property
    def groups(self):
        # GROUP ATTACHMENTRS
        """This property is used to get a list of IAM groups."""
        if not self._groups:
            response = self.iam.list_groups().get("Groups")
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._groups = response
        return self._groups

    @property
    def roles(self):
        # ROLE ATTACHMENTRS
        """This property is used to get a list of IAM roles."""
        if not self._roles:
            response = self.iam.list_roles().get("Roles")
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._roles = response
        return self._roles

    @property
    # POLICY ATTACHMENTRS
    def policies(self):
        """This property is used to get a list of IAM policies."""
        if not self._policies:
            response = self.iam.list_policies(Scope="Local").get("Policies")
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._policies = response
        return self._policies

    @property
    def alias(self):
        """This property is used to get the alias of the account."""
        if not self._alias:
            response = self.iam.list_account_aliases().get("AccountAliases")
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]

            if response:
                self._alias = response[0]
        return self._alias

    def to_dict(self, filtered=True):
        if not filtered:
            return {
                "Users": self.users,
                "Groups": self.groups,
                "Roles": self.roles,
                "Policies": self.policies,
            }

        return {
            "Users": filter_and_sort_dict_list(
                self.users,
                [
                    "Account",
                    "UserName",
                    "PasswordLastUsed",
                    "Groups",
                    "Policies",
                    "AttachedPolicies",
                    "AccessKeys",
                    "MFADevices",
                    "CreateDate",
                ],
            ),
            "Groups": filter_and_sort_dict_list(
                self.groups,
                [
                    "Account",
                    "GroupName",
                    "Arn",
                    "CreateDate",
                ],
            ),
            "Roles": filter_and_sort_dict_list(
                self.roles,
                [
                    "Account",
                    "RoleName",
                    "Description",
                    "Arn",
                    "CreateDate",
                ],
            ),
            "Policies": filter_and_sort_dict_list(
                self.policies,
                [
                    "Account",
                    "PolicyName",
                    "AttachmentCount",
                    "Arn",
                    "CreateDate",
                    "UpdateDate",
                ],
            ),
        }
