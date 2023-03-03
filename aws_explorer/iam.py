from typing import Dict, List

import boto3

from .utils import filter_and_sort_dict_list


class IAMManager:
    """This class is used to manage IAM resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.session = session
        self.client = self.session.client("iam")

    @property
    def users(self) -> List[Dict]:
        result: List[Dict] = []
        for i in self.client.list_users()["Users"]:
            _user: Dict = {
                "Account": self.session.profile_name,
                "Groups": self.client.list_groups_for_user(UserName=i["UserName"]).get("Groups", []),
                "Policies": self.client.list_user_policies(UserName=i["UserName"]).get("PolicyNames", []),
                "AttachedPolicies": self.client.list_attached_user_policies(UserName=i["UserName"]).get(
                    "AttachedPolicies", []
                ),
                "AccessKeys": self.client.list_access_keys(UserName=i["UserName"]).get("AccessKeyMetadata", []),
                "MFADevices": self.client.list_mfa_devices(UserName=i["UserName"]).get("MFADevices", []),
                **i,
            }
            result.append(_user)
        return result

    @property
    def groups(self) -> List[Dict]:
        result: List[Dict] = []
        for i in self.client.list_groups()["Groups"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def roles(self) -> List[Dict]:
        result: List[Dict] = []
        for i in self.client.list_roles()["Roles"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    @property
    def policies(self) -> List[Dict]:
        result: List[Dict] = []
        for i in self.client.list_policies(Scope="Local")["Policies"]:
            result.append({"Account": self.session.profile_name, **i})
        return result

    def get_alias(self) -> str | None:
        result = self.client.list_account_aliases().get("AccountAliases")
        if not result:
            return None
        return result[0]

    def to_dict(self, filtered: bool = True) -> Dict[str, List[Dict]]:
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
