# Snowflake Connector for Python

[Preview Feature](/release-notes/preview-features) — Snowflake Connector for Python 5.x

Snowflake Connector for Python 5.x, built on the Universal Core, is in public preview. It keeps the PEP 249 interface, the `snowflake.connector` module name, and the `snowflake-connector-python` package name. This page documents 4.x, which remains the default and the version Snowflake recommends for production.

See [Snowflake Connector for Python built on the Universal Core](/developer-guide/python-connector/python-connector-universal-core).

Note

This driver currently does not support GCP regional endpoints. Please ensure that any workloads using through this driver do not require support for regional endpoints on GCP. If you have questions about this, please contact Snowflake Support.

The Snowflake Connector for Python provides an interface for developing Python applications that can connect to Snowflake and perform all standard operations. It provides a programming alternative to
developing applications in Java or C/C++ using the Snowflake JDBC or ODBC drivers.

The connector is a native, pure Python package that has no dependencies on JDBC or ODBC. It can be installed using `pip` on
Linux, MacOS, and Windows platforms where Python is installed.

The connector supports developing applications using the Python Database API v2 specification (PEP-249), including using the following standard API objects:

- `Connection` objects for connecting to Snowflake.
- `Cursor` objects for executing DDL/DML statements and queries.

For more information, see [PEP-249](https://www.python.org/dev/peps/pep-0249/).

[SnowSQL](/user-guide/snowsql), the command-line client provided by Snowflake, is an example of an application developed using the connector.

Note

Snowflake now provides first-class Python APIs for managing core Snowflake resources including databases, schemas, tables, tasks, and
warehouses, without using SQL. For more information, see [Snowflake Python APIs: Managing Snowflake objects with Python](/developer-guide/snowflake-python-api/snowflake-python-overview).

**Next Topics:**

- [Installing the Python Connector](/developer-guide/python-connector/python-connector-install)
- [Using the Python Connector](/developer-guide/python-connector/python-connector-example)
- [Using pandas DataFrames with the Python Connector](/developer-guide/python-connector/python-connector-pandas)
- [Distributing workloads that fetch results with the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-distributed-fetch)
- [Using the Snowflake SQLAlchemy toolkit with the Python Connector](/developer-guide/python-connector/sqlalchemy)
- [Python Connector API](/developer-guide/python-connector/python-connector-api)
- [Dependency management policy for the Python Connector](/developer-guide/python-connector/python-connector-dependencies)
