# Snowflake Connector for Python

The Snowflake Connector for Python provides an interface for developing Python applications that can connect to Snowflake and perform all standard operations. It provides a programming alternative to
developing applications in Java or C/C++ using the Snowflake JDBC or ODBC drivers.

Starting with version 5.0, the connector is built on the [Universal Core](/developer-guide/universal-core/universal-core). The public interface remains the `snowflake.connector` module and PEP 249 `Connection` and `Cursor` objects. It can be installed using `pip` on
Linux, macOS, and Windows where Python 3.11 or later is installed.

Note

If you are upgrading from a version before 5.0, see [Upgrading to the Snowflake Connector for Python 5.x](/developer-guide/python-connector/python-connector-upgrade).

The connector supports developing applications using the Python Database API v2 specification (PEP-249), including using the following standard API objects:

- `Connection` objects for connecting to Snowflake.
- `Cursor` objects for executing DDL/DML statements and queries.

For more information, see [PEP-249](https://www.python.org/dev/peps/pep-0249/).

Note

Snowflake now provides first-class Python APIs for managing core Snowflake resources including databases, schemas, tables, tasks, and
warehouses, without using SQL. For more information, see [Snowflake Python APIs: Managing Snowflake objects with Python](/developer-guide/snowflake-python-api/snowflake-python-overview).

**Next Topics:**

- [Installing the Python Connector](/developer-guide/python-connector/python-connector-install)
- [Upgrading to the Snowflake Connector for Python 5.x](/developer-guide/python-connector/python-connector-upgrade)
- [Using the Python Connector](/developer-guide/python-connector/python-connector-example)
- [Using asynchronous I/O with the Python Connector](/developer-guide/python-connector/python-connector-asyncio)
- [Using Pandas with the Python Connector](/developer-guide/python-connector/python-connector-pandas)
- [Distributing workloads that fetch results with the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-distributed-fetch)
- [Snowflake SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy)
- [Python Connector API](/developer-guide/python-connector/python-connector-api)
- [Dependency management policy for the Python Connector](/developer-guide/python-connector/python-connector-dependencies)
