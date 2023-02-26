#!/usr/bin/env python
import logging
import sys

from .account import Account
from .cloudformation import CloudFormationManager
from .ec2 import EC2Manager
from .iam import IAMManager
from .logger import configure_logging
from .s3 import S3Manager
from .sts import STSManager

# configure the logger for your package
configure_logging()
