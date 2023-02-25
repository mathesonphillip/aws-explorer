#!/usr/bin/env python

# Imports
from aws_explorer import Account
import json

account = Account()

print(account)


# print(type(account))

# Print the account object
# print("")
# print(f"Raw: { account }")
# print(f"Account: { account.id }")
# print(f"User: { account.user }")

# Print account resource detaiuls
# print("")
# print(account.iam.alias)
# print(account.s3.buckets)
# print(account.iam.users)
print(account.__dict__)

# ---------------------------------------------------------------------------- #
