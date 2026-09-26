# Setting up your development environment for Snowpark Python

Set up your preferred local development environment to build client applications with Snowpark Python.

If you are writing a stored procedure with Snowpark Python, consider setting up a
[Python worksheet](/developer-guide/snowpark/python/python-worksheets) instead.

## Prerequisites

Use the following SQL query to see which Python versions are enabled in your Snowflake account:

Copy code

```
SELECT DISTINCT runtime_version
FROM SNOWFLAKE.INFORMATION_SCHEMA.PACKAGES
WHERE language = 'python'
AND runtime_version IS NOT NULL
ORDER BY runtime_version;
```

This query returns all versions including those that are deprecated.

Generally available versions:

- 3.9 (deprecated)
- 3.10
- 3.11
- 3.12
- 3.13
- 3.14

Note

- Python 3.9 (deprecated) depends on Snowpark client version 1.5.0.
- Python 3.10 depends on Snowpark client version 1.5.1.
- Python versions 3.11, 3.12, and 3.13 depend on Snowpark client version 1.9.0.

You can create a Python virtual environment for a particular Python version using tools like
[Anaconda](https://www.anaconda.com/),
[Miniconda](https://docs.conda.io/en/latest/miniconda.html), or
[virtualenv](https://docs.python.org/3/tutorial/venv.html).

For example, to use conda to create a Python 3.12 virtual environment, add the Snowflake conda channel,
and install the numpy and pandas packages, type:

Copy code

```
conda create --name py12_env --override-channels -c https://repo.anaconda.com/pkgs/snowflake python=3.12 numpy pandas pyarrow
```

Creating a new conda environment locally with the Snowflake channel is recommended
in order to have the best experience when using UDFs. For more information, see
[Local development and testing](/developer-guide/udf/python/udf-python-packages#label-python-udfs-anaconda-local-testing).

Note

There is a known issue with running Snowpark Python on Apple M1 chips due to memory handling in pyOpenSSL.
The error message displayed is, “Cannot allocate write+execute memory for ffi.callback()”.

As a workaround, set up a virtual environment that uses x86 Python using these commands:

Copy code

```
CONDA_SUBDIR=osx-64 conda create -n snowpark python=3.12 numpy pandas pyarrow --override-channels -c https://repo.anaconda.com/pkgs/snowflake
conda activate snowpark
conda config --env --set subdir osx-64
```

Then, install Snowpark within this environment as described in the next section.

### Prerequisites for using Pandas DataFrames

The Snowpark API provides methods for writing data to and from Pandas DataFrames.
[Pandas](https://pandas.pydata.org/) is a library for data analysis.
With Pandas, you use a data structure called a DataFrame to analyze and manipulate two-dimensional data.

These methods require the following libraries:

- Pandas 1.0.0 (or higher).
- [PyArrow library](https://arrow.apache.org/docs/python/) version 8.0.0.

Note

If you have already installed any version of the PyArrow library other than the recommended
version listed above, uninstall PyArrow before installing Snowpark.

Installing Snowpark using pip automatically installs the appropriate version of PyArrow.
If you use conda to install Snowpark, you must specify `pyarrow` in the list of packages.

Do not re-install a different version of PyArrow after installing Snowpark.

## Installation instructions

Note

Before running the commands in this section, make sure you are in a Python environment for a supported Python version.
You can check this by typing the command `python -V`. If the version displayed is not a supported version,
refer to the previous section.

Install the Snowpark Python package into the Python virtual environment by using `conda` or `pip`.

Copy code

```
conda install snowflake-snowpark-python
```

-or-

Copy code

```
pip install snowflake-snowpark-python
```

Optionally, specify packages that you want to install in the environment such as,
for example, the Pandas data analysis package:

Copy code

```
conda install snowflake-snowpark-python pandas pyarrow
```

-or-

Copy code

```
pip install "snowflake-snowpark-python[pandas]"
```

You can view the Snowpark Python project description on
[the Python Package Index (PyPi) repository](https://pypi.org/project/snowflake-snowpark-python/).

## Next step: Connect to Snowflake

After installing Snowpark, [create a session](/developer-guide/snowpark/python/creating-session) to authenticate and connect to Snowflake from your Python application. The session guide explains how to use a named connection from `connections.toml` or pass connection parameters to `Session.builder`.

Snowpark uses the authentication mechanisms supported by the Snowflake Connector for Python. For authentication options, including single sign-on (SSO), multi-factor authentication (MFA), and key pair authentication, see [Connecting to Snowflake with the Python Connector](/developer-guide/python-connector/python-connector-connect).

## Setting up Snowflake Notebooks for Snowpark

You can use the Snowflake Notebooks development environment to perform data science and data engineering workflows with Python. Snowflake Notebooks
comes preinstalled with Snowpark for Python.

For more information about getting started with Snowflake Notebooks, see [Getting started with Legacy Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-get-started).

For information about setting up Snowflake Notebooks, see [Set up Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-setup).

For more information about using the Snowpark library in Snowflake Notebooks, see [Snowpark Python in notebooks](/user-guide/ui-snowsight/notebooks-use-with-snowflake#label-notebooks-snowpark).

## Setting up a Jupyter notebook for Snowpark

To get started using Snowpark with Jupyter Notebooks, do the following:

1. Install Jupyter Notebooks:

   Copy code

   ```
   pip install notebook
   ```
2. Start a Jupyter Notebook:

   Copy code

   ```
   jupyter notebook
   ```
3. In the top-right corner of the web page that opened, select **New** » **Python 3 Notebook**.
4. In a cell, create a session. For more information, see [Creating a Session](/developer-guide/snowpark/python/creating-session#label-snowpark-python-creating-session).

## Setting up an IDE for Snowpark

You can use Snowpark with an integrated development environment (IDE).

To use Snowpark with Microsoft Visual Studio Code,
[install the Python extension and then specify the Python environment to use](https://code.visualstudio.com/docs/languages/python).

To use features for authoring and debugging Snowpark Python stored procedures in VS Code, install the [Snowflake Extension for Visual Studio Code](/user-guide/vscode-ext). The
extension enables you to connect to Snowflake and execute SQL statements directly in VS Code.

Important

You must manually select the Python environment that you created when you set up your development environment.
To do this, use the `Python: Select Interpreter` command from the `Command Palette`.
For more information, see [Using Python environments in VS Code](https://code.visualstudio.com/docs/python/environments)
in the Microsoft Visual Studio documentation.

## Importing modules

The main classes for the Snowpark API are in the `snowflake.snowpark` module.

To import particular names from a module, specify the names. For example:

Copy code

```
>>> from snowflake.snowpark.functions import avg
```
