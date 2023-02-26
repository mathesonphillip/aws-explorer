#!/usr/bin/env python
import logging
import sys

from .account import Account
from .backup import BackupManager
from .cloudformation import CloudFormationManager
from .ec2 import EC2Manager
from .ecs import ECSManager
from .iam import IAMManager
from .lambda_manager import LambdaManager
from .logger import configure_logging
from .s3 import S3Manager
from .sts import STSManager

# configure the logger for your package
configure_logging()
