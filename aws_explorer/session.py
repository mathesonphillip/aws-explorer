"""Represent an AWS session.

The session class is used to initialise and interact with the aws services that are supported by the tool.
"""

from boto3 import Session as Boto3Session
import botocore.exceptions as botoexceptions
from .utils import get_logger
from collections import namedtuple


from .s3 import S3Manager
from .iam import IAMManager
from .sts import STSManager

# --------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #

log = get_logger(__name__)


# Where to store all the type data?
class InvalidSessionConfigError(Exception):

    """Raised when session configuration is invalid."""


Identity = namedtuple("Identity", ["account_id", "user_id", "arn"])
Credentials = namedtuple("Credentials", ["access_key", "secret_key"])
SessionRepr = namedtuple("Session", ["profile", "region"])
Service = namedtuple("Service", ["name", "service_type"])

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

SERVICES = [
    Service("sts", STSManager),
    Service("s3", S3Manager),
    Service("iam", IAMManager),
    # Service("ec2", EC2Manager),
    # Service("ssm", SSMManager),
]

# ---------------------------------------------------------------------------- #
# logger = get_logger(__name__)


# TODO: Add doc strings
class Session:
    def __init__(
        self,
        profile: str | None = None,
        region: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
    ) -> None:
        log.info(f"Creating session with profile: {profile}, region: {region}, access_key: {access_key}, secret_key: {secret_key}")
        log.warning(f"Creating session with profile: {profile}, region: {region}, access_key: {access_key}, secret_key: {secret_key}")

        # print(f"Creating session with profile: {profile}, region: {region}, access_key: {access_key}, secret_key: {secret_key}")

        try:
            self._session = self._create_session(profile, region, access_key, secret_key)
        except InvalidSessionConfigError:
            raise

        self._services: list[Service] = []
        self._init_services()

    # ------------------------------------------------------------------------ #

    @property
    def config(self) -> SessionRepr:
        return SessionRepr(self._session.profile_name, self._session.region_name)

    @property
    def credentials(self) -> Credentials:
        return Credentials(self._session.get_credentials().access_key, self._session.get_credentials().secret_key)

    @property
    def identity(self) -> Identity:
        response = self._session.client("sts").get_caller_identity()
        return Identity(response["Account"], response["UserId"], response["Arn"])

    @property
    def services(self) -> list[Service]:
        return self._services

    # ------------------------------------------------------------------------ #

    def _create_session(
        self,
        profile: str | None = None,
        region: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
    ) -> Boto3Session:
        """Create a boto3 session."""

        session_args: dict[str, str] = {}

        # Check that either profile or credentials are provided
        if profile is not None and (access_key or secret_key):
            raise InvalidSessionConfigError("Must provide either profile or credentials")

        # Check that if profile is not provided, both credentials are provided
        if profile is None and (access_key and not secret_key) or (secret_key and not access_key):
            raise InvalidSessionConfigError("Not enough credentials provided")
        # -------------------------------------------------------------------- #

        if profile:
            session_args.update({"profile_name": profile})

        if access_key and secret_key:
            session_args.update({"aws_access_key_id": access_key, "aws_secret_access_key": secret_key})

        try:
            return Boto3Session(**session_args, region_name=region)
        except botoexceptions.ProfileNotFound as error:
            raise InvalidSessionConfigError(f"Profile {profile} not found") from error
        except botoexceptions.NoRegionError as error:
            raise InvalidSessionConfigError("No region provided") from error

    # def __repr__(self) -> str:
    #     repr_str = f"<Session session={self.config.profile}, services={self.services}>"
    #     return repr_str

    # ------------------------------------------------------------------------ #

    def _init_services(self) -> None:
        """Initialise resource services."""

        for service in SERVICES:
            log.debug(f"Initialising {service}")

            instantiated_service = service.service_type(self._session)

            setattr(self, service.name, instantiated_service)

            self._services.append(Service(service.name, instantiated_service))

        print(self._services)

    # def export_to_json(self, obj: Any, export_path: str) -> None:
    #     """Export the provided object to JSON

    #     :param obj: The object to export
    #     :param export_path: The path to export to

    #     """
    #     with open(export_path, "w", encoding="utf8") as file:
    #         file.write(json.dumps(obj))

    # def export_to_yaml(self, obj: Any, export_path: str) -> None:
    #     """Export the provided object to YAML

    #     :param obj: The object to export
    #     :param export_path: The path to export to

    #     """
    #     with open(export_path, "w", encoding="utf8") as file:
    #         yaml.dump(obj, file)

    # def export_to_excel(self, obj: Any, export_path: str) -> None:
    #     """Export the provided object to Excel

    #     :param obj: The object to export
    #     :param export_path: The path to export to

    #     """
    #     data_dict = remove_timezones_from_object(obj)

    #     # pylint: disable=abstract-class-instantiated
    #     with pd.ExcelWriter(path=export_path) as writer:
    #         # iterate over the top-level keys in the dictionary
    #         for service_key in data_dict:  # type: ignore
    #             for key, data in data_dict[service_key].items():  # type: ignore
    #                 sheet_name = f"{service_key}.{key}"

    #                 print(f"Writing {sheet_name} to Excel")

    #                 df = pd.DataFrame(data)
    #                 df.to_excel(
    #                     writer,
    #                     sheet_name=sheet_name,
    #                     startrow=1,
    #                     header=False,
    #                     index=False,
    #                 )

    #                 column_settings: list[dict[str, str]] = [{"header": column} for column in df.columns]

    #                 worksheet = writer.sheets[sheet_name]
    #                 worksheet.add_table(
    #                     0,
    #                     0,
    #                     len(df),
    #                     len(df.columns) - 1,
    #                     {"name": sheet_name, "columns": column_settings},
    #                 )

    #                 # Set the column width to the max length of the column header
    #                 for column in df:
    #                     column_length = max(df[column].astype(str).map(len).max(), len(column))  # type: ignore
    #                     col_idx = df.columns.get_loc(column)
    #                     writer.sheets[sheet_name].set_column(col_idx, col_idx, column_length)

    # def get_filename(self, extension: str) -> str:
    #     """Get the filename for the export file
    #     Filename format: <profile_name>_<%Y%m%s>.<extension>

    #     :param extension: The file extension to use
    #     :return: The filename

    #     """
    #     timestamp = datetime.now().strftime("%Y%m%d")
    #     return f"{self.session.profile_name}_{timestamp}.{extension}"

    # def export(self, extension: str, export_path: str = ".") -> None:
    #     """This method is used to export the session to a file.
    #     The file extension is used to determine the file type.

    #     :param extension: The file extension to use
    #     :param export_path: The path to export to
    #     """
    #     # Define a dictionary with file extensions and corresponding file
    #     # writing functions
    #     file_writers = {
    #         "json": self.export_to_json,
    #         "yaml": self.export_to_yaml,
    #         "xlsx": self.export_to_excel,
    #     }

    #     # Get the file writing function corresponding to the file extension
    #     file_writer: Optional[Callable[[Any, str], None]] = file_writers.get(extension)

    #     if file_writer is None:
    #         raise ValueError(f"Unsupported file extension: {extension}")

    #     # Get the filename and full export path
    #     filename = self.get_filename(extension)
    #     full_export_path = f"{export_path}/{filename}"

    #     # Call the file writing function with the object and export path
    #     file_writer(self.to_dict(), full_export_path)

    # def __repr__(self) -> str:
    #     """Return the object representation"""

    #     return f"{type(self).__name__}({self.session.profile_name})"
