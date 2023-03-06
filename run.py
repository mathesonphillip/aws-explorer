#! /usr/bin/env python

"""Demo script used to run the application.

Primary purpose is for testing and development.
But this can also serve as an exampole of how to use the application.
"""

import os
# from dotenv import load_dotenv

from aws_explorer import Session

# Load environment variables from .env file
# load_dotenv()

# ---------------------------------------------------------------------------- #
#                                  EXAMPLE_01                                  #
# ---------------------------------------------------------------------------- #


def session_from_named_profile():
    """Instantiate a named profile session.

    Pass a valid named profile to the from_named_profile method.
    boto3 will lookup the named profile in the ~/.aws/credentials file
        and use the credentials to instantiate the session.
    """

    session = Session(profile="aws-explorer-demo", region="ap-southeast-2")
    print(session.sts.identity)


# ---------------------------------------------------------------------------- #
#                                  EXAMPLE_02                                  #
# ---------------------------------------------------------------------------- #


def session_from_default_profile():
    """Instantiate the default session.
    If no credentials are provided,
        boto3 resorts to using the default named profile.
    """

    session = Session()
    print(session.sts.identity)


# ---------------------------------------------------------------------------- #
#                                  EXAMPLE_03                                  #
# ---------------------------------------------------------------------------- #


def session_from_credentials():
    """Instantiate an session object through passing credentials."""

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    session = Session.from_credentials(access_key, secret_key)
    print(session.sts.identity)


# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #


def main():
    # EXAMPLE_01
    session_from_named_profile()

    # EXAMPLE_02
    # session_from_default_profile()

    # EXAMPLE_03
    # session_from_credentials()


if __name__ == "__main__":
    main()
