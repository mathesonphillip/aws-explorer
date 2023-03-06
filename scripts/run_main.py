#!/usr/bin/env python

# Imports

from aws_explorer import Session

session = Session()

print(session)


# print(type(session))

# Print the session object
# print("")
# print(f"Raw: { session }")
# print(f"session: { session.id }")
# print(f"User: { session.user }")

# Print session resource detaiuls
# print("")
# print(session.iam.alias)
# print(session.s3.buckets)
# print(session.iam.users)
print(session.__dict__)

# ---------------------------------------------------------------------------- #
