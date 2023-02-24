# MISC

A file for miscellaneous notes and thoughts


```bash
# Install the package in editable mode
# This will allow you to make changes to the package and see the changes reflected in your Jupyter Notebook

pip install -editable /path/to/your/package

```



<!-- ----------------------------------------------------------------------- -->



## Build

To build the project, run the following commands:


```bash {cmd=true }
python setup.py sdist bdist_wheel
pip install aws-explorer
```