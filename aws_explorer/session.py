"""Represent an AWS session.

The session class is used to initialise and interact with the aws services that are supported by the tool.
"""

from boto3 import Session as Boto3Session
import botocore.exceptions as botoexceptions
from .utils import get_logger
from rich import print
from rich import print_json
from rich.pretty import pprint
from .s3 import S3Manager
from .iam import IAMManager
from .ec2 import EC2Manager
from .ssm import SSMManager

from .sts import STSManager
import json
import rich.repr

from .types import Profile, Credentials, ResourceManager, Identity, ResourceManager2

log = get_logger(__name__)


# Where to store all the type data?
class InvalidSessionConfigError(Exception):
    ...


# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

SERVICES = [
    ResourceManager(name="sts", service_class=STSManager),
    ResourceManager(name="s3", service_class=S3Manager),
    ResourceManager(name="iam", service_class=IAMManager),
    ResourceManager(name="ec2", service_class=EC2Manager),
    ResourceManager(name="ssm", service_class=SSMManager),
]


class Session:
    def __init__(self, session_configuration: Profile | Credentials) -> None:
        log.info("Creating Session: %s", repr(session_configuration))

        self._session_configuration = session_configuration

        try:
            self._session = Boto3Session(**session_configuration.dict())
        except botoexceptions.ProfileNotFound as error:
            raise InvalidSessionConfigError(f"Profile {session_configuration.profile_name} not found") from error

        # FIXME: Fix data type
        self._services: list[ResourceManager] = []
        self._init_services()

    # ------------------------------------------------------------------------ #

    def _init_services(self) -> None:
        """Initialise resource services."""
        log.info("Initialising services")

        for service in SERVICES:
            log.debug(f"Initialising {service}")

            instantiated_service = service.service_class(self)

            setattr(self, service.name, instantiated_service)

            self._services.append(ResourceManager2(name=service.name, service_class=instantiated_service))

    # ------------------------------------------------------------------------ #

    @property
    def session(self) -> Boto3Session:
        return self._session

    @property
    def identity(self) -> Identity:
        return self.sts.identity

    @property
    def session_configuration(self) -> Profile | Credentials:
        return self._session_configuration

    @property
    def credentials(self) -> Credentials:
        return self._session.get_credentials().__dict__

    @property
    def services(self) -> list[ResourceManager]:
        return self._services

    # Get report data
    def export(self) -> dict:
        print("Exporting account resources")
        data = {}

        for service in self.services:
            if not hasattr(service.service_class, "export"):
                continue

            print(f"Exporting {service.name} resources")
            data[service.name] = service.service_class.export()
            # print size of data
            print(f"Size of {service.name} data: {len(data[service.name])}")
            # data[service.name] = service.get_report_data()

        return data

    # ------------------------------------------------------------------------ #
