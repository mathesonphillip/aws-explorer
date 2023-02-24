# aws-explorer

[![Build Status](https://travis-ci.org/awslabs/aws-explorer.svg?branch=master)](https://travis-ci.org/awslabs/aws-explorer)

`aws-explorer` is a Python package that provides a convenient and consistent way to manage, query and report on AWS resources using the AWS SDK for Python (Boto3). The package is designed to be used in Jupyter Notebooks, and provides importable modules for each AWS service, with classes for each resource type, and methods to help manage, query and report on the resource type.


## Project Structure

```bash{cmd=true hide=true run_on_save}

# Output the tree structure of the project
tree .. --gitignore --dirsfirst --noreport --sort=name -I "__pycache__"

```

## Installation

The `aws-explorer` package can be installed using pip:

```
pip install aws-explorer
```

Alternatively, you can install the package from the source code:

```bash
git clone https://github.com/your-username/aws-explorer.git
cd aws-explorer
python setup.py install
```

## Usage

To use the `aws-explorer` package in your Jupyter Notebook, follow the code snippet below:

```python
#Import the modules
from aws_explorer import Account

# You can then create an "Account" object
dev = Account(profile_name='dev')

# You can then use the "Account" object to manage, query and report on the AWS resources
instances = dev.ec2.instances
buckets = dev.s3.buckets

# Interact with the AWS resources
for instance in instances:
    print(instance.id)

# For example, you can use the "instances" and "buckets" variables to create a pandas DataFrame
import pandas as pd
df_instances = pd.DataFrame(instances)
df_buckets = pd.DataFrame(buckets)
```
<!-- For more information on how to use the aws-explorer package, please refer to the documentation. -->

## Contributing

Contributions to the `aws-explorer` package are welcome! If you find a bug, have a feature request, or would like to contribute code, please create a new issue or pull request on the GitHub repository.

Before contributing, please read the `CONTRIBUTING.md` file for guidelines on how to contribute to the project.

## License

The `aws-explorer` package is licensed under the MIT License. See the `LICENSE.md` file for more information.



<!-- -------------------------------- Links -------------------------------- -->

[Boto3]: https://boto3.readthedocs.io/en/latest/
[AWS CLI]: https://aws.amazon.com/cli/

<!-- ---------------------------- Abbreviations ----------------------------- -->

*[AWS]: Amazon Web Services
