from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any


class Identity(BaseModel):
    alias: str | None = None
    account_id: str
    user_id: str
    arn: str

    class Config:
        fields = {
            "account_id": "Account",
            "user_id": "UserId",
            "arn": "Arn",
        }


# How do get to import a different model and convert it to a pydantic model?
class Bucket(BaseModel):
    name: str
    creation_date: datetime
    location: str | None = None
    encryption: dict | None = None

    class Config:
        fields = {
            "name": "Name",
            "creation_date": "CreationDate",
        }


class Credentials(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str = "ap-southeast-2"


class Profile(BaseModel):
    profile_name: str | None = None
    region_name: str = "ap-southeast-2"

    # def __repr__(self) -> str:
    #     return f"<Profile profile_name={self.profile_name} region_name={self.region_name}>"


class SessionConfig(BaseModel):
    method: Profile | Credentials


class ResourceManager(BaseModel):
    name: str
    service_class: type


class ResourceManager2(BaseModel):
    name: str
    service_class: object


class Group(BaseModel):
    group_name: str
    group_id: str
    arn: str
    create_date: datetime

    class Config:
        fields = {
            "group_name": "GroupName",
            "group_id": "GroupId",
            "arn": "Arn",
            "create_date": "CreateDate",
        }


class AccessKey(BaseModel):
    user_name: str
    access_key_id: str
    status: str
    create_date: datetime

    class Config:
        fields = {
            "user_name": "UserName",
            "access_key_id": "AccessKeyId",
            "status": "Status",
            "create_date": "CreateDate",
        }


class Policy(BaseModel):
    policy_name: str
    policy_id: str
    arn: str
    path: str
    default_version_id: str
    attachment_count: int
    permissions_boundary_usage_count: int
    is_attachable: bool
    create_date: datetime
    update_date: datetime

    class Config:
        fields = {
            "policy_name": "PolicyName",
            "policy_id": "PolicyId",
            "arn": "Arn",
            "path": "Path",
            "default_version_id": "DefaultVersionId",
            "attachment_count": "AttachmentCount",
            "permissions_boundary_usage_count": "PermissionsBoundaryUsageCount",
            "is_attachable": "IsAttachable",
            "create_date": "CreateDate",
            "update_date": "UpdateDate",
        }


class Role(BaseModel):
    role_name: str
    description: str | None = None
    role_id: str
    arn: str
    path: str
    create_date: datetime
    assume_role_policy_document: dict
    description: str
    max_session_duration: int

    class Config:
        fields = {
            "role_name": "RoleName",
            "role_id": "RoleId",
            "arn": "Arn",
            "path": "Path",
            "create_date": "CreateDate",
            "assume_role_policy_document": "AssumeRolePolicyDocument",
            "description": "Description",
            "max_session_duration": "MaxSessionDuration",
        }


class MFADevice(BaseModel):
    user_name: str
    serial_number: str
    enable_date: datetime

    class Config:
        fields = {
            "user_name": "UserName",
            "serial_number": "SerialNumber",
            "enable_date": "EnableDate",
        }


class User(BaseModel):
    user_name: str
    user_id: str
    arn: str
    create_date: datetime
    password_last_used: datetime | None = None
    groups: list[Group] = Field(default_factory=list)
    policies: list[Policy] = Field(default_factory=list)
    attached_policies: list[Policy] = Field(default_factory=list)
    mfa_devices: list[MFADevice] = Field(default_factory=list)
    access_keys: list[AccessKey] = Field(default_factory=list)

    class Config:
        fields = {
            "user_name": "UserName",
            "user_id": "UserId",
            "arn": "Arn",
            "create_date": "CreateDate",
            "password_last_used": "PasswordLastUsed",
        }


class Instance(BaseModel):
    AccountId: str | None = None
    AccountName: str | None = None
    Name: str | None = None
    SSMManaged: bool | None = None
    VpcName: str | None = None
    SubnetName: str | None = None
    AmiLaunchIndex: int
    ImageId: str
    InstanceId: str
    InstanceType: str
    KeyName: str | None = None
    LaunchTime: datetime
    Monitoring: dict[str, str]
    Placement: dict[str, str]
    PrivateDnsName: str
    PrivateIpAddress: str
    # ProductCodes: list[str]
    PublicDnsName: str
    State: dict[str, str]
    StateTransitionReason: str
    SubnetId: str
    VpcId: str
    Architecture: str
    # BlockDeviceMappings: list[dict[str, Any]]
    ClientToken: str
    EbsOptimized: bool
    EnaSupport: bool
    Hypervisor: str
    IamInstanceProfile: dict[str, str] | None = None
    # NetworkInterfaces: list[dict[str, Any]]
    RootDeviceName: str
    RootDeviceType: str
    SecurityGroups: list[dict[str, str]]
    SourceDestCheck: bool
    StateReason: dict[str, str] | None = None
    Tags: list[dict[str, str]]
    VirtualizationType: str
    CpuOptions: dict[str, int]
    CapacityReservationSpecification: dict[str, str]
    HibernationOptions: dict[str, bool]
    # MetadataOptions: dict[str, Any]
    EnclaveOptions: dict[str, bool]
    PlatformDetails: str
    UsageOperation: str
    UsageOperationUpdateTime: datetime
    # PrivateDnsNameOptions: dict[str, Any]
    MaintenanceOptions: dict[str, str]

    # class Config:
    #     arbitrary_types_allowed = True


class SecurityGroup(BaseModel):
    AccountId: str | None = None
    AccountName: str | None = None
    GroupName: str | None = None
    Description: str | None = None
    IpPermissions: list[dict[str, Any]]
    Instances: list[tuple] = Field(default_factory=list)
    Tags: list[dict[str, str]] = Field(default_factory=list)
    OwnerId: str
    GroupId: str
    # IpPermissionsEgress: list[dict[str, Any]]
    VpcId: str

    class Config:
        arbitrary_types_allowed = True


class SecurityGroupList(BaseModel):
    __root__: list[SecurityGroup] = Field(default_factory=list)


class SecurityGroupRule(BaseModel):
    AccountId: str | None = None
    AccountName: str | None = None
    GroupName: str | None = None
    SecurityGroupRuleId: str
    GroupId: str
    GroupOwnerId: str
    IsEgress: bool
    IpProtocol: str
    FromPort: int
    ToPort: int
    CidrIpv4: str | None = None
    CidrIpv6: str | None = None
    PrefixListId: str | None = None
    Tags: list[dict[str, str]] = Field(default_factory=list)
    Instances: list[tuple] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


class InstanceSecurityGroupRule(BaseModel):
    AccountId: str | None = None
    AccountName: str | None = None
    InstanceId: str
    InstanceName: str
    IsEgress: bool
    IpProtocol: str
    FromPort: int
    ToPort: int
    CidrIpv4: str | None = None
    CidrIpv6: str | None = None
    PrefixListId: str | None = None
    GroupName: str
    GroupId: str

    class Config:
        arbitrary_types_allowed = True


class InstanceTag(BaseModel):
    AccountId: str | None = None
    AccountName: str | None = None
    InstanceId: str
    InstanceName: str
    Key: str
    Value: str


class SSMInstance(BaseModel):
    AccountId: str | None = None
    AccountName: str | None = None
    InstanceId: str
    InstanceName: str | None = None
    PingStatus: str
    LastPingDateTime: datetime
    AgentVersion: str
    IsLatestVersion: bool
    PlatformType: str
    PlatformName: str
    PlatformVersion: str
    ResourceType: str
    IPAddress: str
    ComputerName: str
    SourceId: str
    SourceType: str


class InstanceSecurityGroup(BaseModel):
    AccountId: str | None = None
    AccountName: str | None = None
    InstanceId: str
    InstanceName: str
    GroupName: str | None = None
    GroupId: str | None = None
