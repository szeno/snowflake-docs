# Setting up a Python development environment

Set up a Python environment compatible with the Snowpark Checkpoints package you install. Snowpark Checkpoints 0.4.0 requires Python 3.9, 3.10, or 3.11; use Python 3.11 for a new environment. These package requirements differ from the Python runtime versions supported by Snowflake UDFs.

Install the `snowpark-checkpoints` package in that environment by following [Install Snowpark Checkpoints](/developer-guide/snowpark/python/checkpoints-installation). The guide includes pip and conda commands for the complete library and its individual packages. Installing the complete library also installs its required dependencies, including Snowpark Python 1.23.0 or later.

## Create a virtual environment

For example, with Python 3.11 installed, create an isolated environment using the built-in `venv` module:

Copy code

```
python3.11 -m venv .venv
```

Activate it on macOS or Linux:

Copy code

```
source .venv/bin/activate
```

On Windows PowerShell, create and activate the environment with:

Copy code

```
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

After activation, verify the interpreter version:

Copy code

```
python --version
```

The output should identify Python 3.11. Then follow [Install Snowpark Checkpoints](/developer-guide/snowpark/python/checkpoints-installation) to install the library in this environment.

## Try the examples

After installation, see these examples for the next steps:

- [Generate Snowpark DataFrames for unit tests](/developer-guide/snowpark/python/checkpoints-hypothesis#examples).
- [Configure Checkpoints logging](/developer-guide/snowpark/python/checkpoints-logging#basic-logging-configuration).
