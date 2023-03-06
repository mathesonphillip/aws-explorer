from collections import namedtuple
from aws_explorer.session import InvalidSessionConfigError

Credentials = namedtuple("Credentials", ["access_key", "secret_key"])

# ---------------------------------------------------------------------------- #

ACCOUNT_ID = "123456789012"

PROFILE = "explorer"

CREDENTIALS = Credentials("AKIAIOSFOAWSEXPLORER", "wJalrXUtnFEMI/K7MDENG/bPxRfiCAWSEXPLORER")

CREDENTIAL_FILE_CONTENTS = f"""
[explorer]
aws_access_key_id = {CREDENTIALS.access_key}
aws_secret_access_key = {CREDENTIALS.secret_key}
"""

BUCKETS = [
    f"test-explorer-mocked-01-{ACCOUNT_ID}",
    f"test-explorer-mocked-02-{ACCOUNT_ID}",
    f"test-explorer-mocked-03-{ACCOUNT_ID}",
    f"test-explorer-mocked-04-{ACCOUNT_ID}",
    f"test-explorer-mocked-05-{ACCOUNT_ID}",
]


TEST_PARAMS = {
    "test_session_init" : [
        # (expected, region, access_key, secret_key)
        # Default Profile
        ("default", None, None, None, None),
        ("default", None, "ap-southeast-2", None, None),
        # Explicit Profile
        ("explorer", "explorer", None, None, None),
        ("explorer", "explorer", "ap-southeast-2", None, None),
        # ("moto", "moto", "ap-southeast-2", None, None),
        (InvalidSessionConfigError, "explorer", None, None, CREDENTIALS.secret_key),
        (InvalidSessionConfigError, "explorer", None, CREDENTIALS.access_key, None),
        (InvalidSessionConfigError, "explorer", None, CREDENTIALS.access_key, CREDENTIALS.secret_key),
        # Credentials
        ("default", None, None, CREDENTIALS.access_key, CREDENTIALS.secret_key),
        ("default", None, "ap-southeast-2", CREDENTIALS.access_key, CREDENTIALS.secret_key),
        (InvalidSessionConfigError, "explorer", "ap-southeast-2", CREDENTIALS.access_key, CREDENTIALS.secret_key),
        (InvalidSessionConfigError, None, None, CREDENTIALS.access_key, None),
        (InvalidSessionConfigError, None, None, None, CREDENTIALS.secret_key),
    ]
}

