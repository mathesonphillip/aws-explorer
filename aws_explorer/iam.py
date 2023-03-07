""" Class module for the IAMManager class, which is used to interact with the AWS IAM service."""

from .types import User, Group, AccessKey, Policy, MFADevice, Role
from functools import cached_property
import boto3


class IAMManager:

    """This class is used to manage IAM resources."""

    def __init__(self, session: boto3.Session) -> None:
        self.parent = session
        self.client = self.parent._session.client("iam")
        self._resources: list[str] = [
            "users",
            "groups",
            "policies",
            "roles",
        ]

    @cached_property
    def users(self) -> list[User]:
        print("Getting users")
        """Return a list of IAM users."""
        users: list[User] = []
        for u in self.client.list_users()["Users"]:
            # Create a User object
            user = User.parse_obj(u)

            # Get the groups the user is in and add them to the user object
            groups = self.client.list_groups_for_user(UserName=user.user_name).get("Groups", [])
            user.groups.append([Group.parse_obj(g) for g in groups])

            # Get the policies the user has and add them to the user object
            policies = self.client.list_user_policies(UserName=user.user_name).get("PolicyNames", [])
            user.policies.append([Policy.parse_obj(p) for p in policies])

            # Get the attached policies the user has and add them to the user object
            # attached_policies = self.client.list_attached_user_policies(UserName=user.user_name).get("AttachedPolicies", [])
            # user.attached_policies.append([AttachedPolicy.parse_obj(p) for p in attached_policies])

            # Get the access keys the user has and add them to the user object
            access_keys = self.client.list_access_keys(UserName=user.user_name).get("AccessKeyMetadata", [])
            user.access_keys.append([AccessKey.parse_obj(k) for k in access_keys])

            # Get the MFA devices the user has and add them to the user object
            mfa_devices = self.client.list_mfa_devices(UserName=user.user_name).get("MFADevices", [])
            user.mfa_devices.append([MFADevice.parse_obj(m) for m in mfa_devices])

            # Add the user to the list of users
            users.append(user)

        return users

    # ------------------------------------------------------------------------ #

    @cached_property
    def groups(self) -> list[Group]:
        """Return a list of IAM groups."""
        groups: list[Group] = []
        for group in self.client.list_groups()["Groups"]:
            # Create a Group object
            groups.append(Group.parse_obj(group))
        return groups

    @cached_property
    def roles(self) -> list[Role]:
        """Return a list of IAM roles."""
        roles: list[Role] = []
        for role in self.client.list_roles()["Roles"]:
            # Create a Role object and add it to the list of roles
            roles.append(Role.parse_obj(role))
        return roles

    @cached_property
    def policies(self) -> list[Policy]:
        """Return a list of IAM policies."""
        policies: list[Policy] = []
        for policy in self.client.list_policies(Scope="Local")["Policies"]:
            # Create a Policy object
            policies.append(Policy.parse_obj(policy))
        return policies

    @cached_property
    def alias(self) -> str | None:
        """Return the session alias."""
        try:
            return self.client.list_account_aliases()["AccountAliases"][0]
        except IndexError:
            return None

    def export(self):
        print("Exporting IAM resources...")
        export_data = {}
        for resource_type in self._resources:
            print(f"Exporting {resource_type}...")

            export_data[resource_type] = []
            for i in resource_type:
                resource_data = getattr(self, resource_type)
                for resource in resource_data:
                    export_data[resource_type].append(resource.dict(exclude_none=True))
        return export_data
