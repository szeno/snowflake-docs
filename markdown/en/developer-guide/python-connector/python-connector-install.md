# Installing the Python Connector

[Preview Feature](/release-notes/preview-features) — Snowflake Connector for Python 5.x

The instructions on this page install the 4.x connector.

Snowflake Connector for Python 5.x, built on the Universal Core, is in public preview. Because both lines use the `snowflake-connector-python` package name, it installs into a separate virtual environment. See [Installing the release candidate](/developer-guide/python-connector/python-connector-universal-core#label-python-universal-core-install).

To install the latest Python Connector for Snowflake, use:

> Copy code
>
> ```
> pip install snowflake-connector-python
> ```

If you won’t use Snowflake on AWS, you can exclude the `boto3` and `botocore` dependencies for AWS. These libraries take up both disk space and memory in the Python Connector, even when you don’t need them. To disable these libraries, set the `SNOWFLAKE_NO_BOTO` environment variable to `true` during installation:

> Copy code
>
> ```
> SNOWFLAKE_NO_BOTO=true pip install snowflake-connector-python
> ```

The source code for the Python driver is available on [GitHub](https://github.com/snowflakedb/snowflake-connector-python).

## Prerequisites

Requires Python version 3.9 (deprecated) or later.

For a list of the operating systems supported by Snowflake clients, see [Operating system support](/release-notes/requirements#label-client-operating-system-support).
