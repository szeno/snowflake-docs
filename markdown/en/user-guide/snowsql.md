# SnowSQL (CLI client)

Caution

[Snowflake CLI](/developer-guide/snowflake-cli/index) is the preferred command-line client for new installs and new work. SnowSQL is a
legacy command-line client. Snowflake will only add new features and enhancements to Snowflake CLI. Snowflake supports SnowSQL 1.5.x through
April 16, 2028. Earlier minor versions have earlier support end dates.

If you’re starting a new project, [install Snowflake CLI](/developer-guide/snowflake-cli/installation/installation). If you already use
SnowSQL, see [Migrating from SnowSQL to Snowflake CLI](/user-guide/snowsql-migrate).

SnowSQL is a command-line client for connecting to Snowflake to execute SQL queries and perform all DDL and DML operations, including loading data into and unloading data out of database tables.

## Support dates

As of July 2025, Snowflake provides support based on the minor releases for SnowSQL, as follows:

| SnowSQL version | Initial release date | Support end date |
| --- | --- | --- |
| 1.2.x | February 02, 2023 | December 19, 2025 |
| 1.3.x | May 02, 2024 | May 02, 2026 |
| 1.4.x | May 22, 2025 | May 22, 2027 |
| 1.5.x | April 16, 2026 | April 16, 2028 |

Expand

Show lessSee more

SnowSQL (`snowsql` executable) can be run as an interactive shell or in batch mode through `stdin` or using the `-f` option.

SnowSQL is an example of an application developed using the [Snowflake Connector for Python](/developer-guide/python-connector/python-connector); however, the connector is not a prerequisite for installing SnowSQL. All required software for installing SnowSQL
is bundled in the installers.

Snowflake provides platform-specific versions of SnowSQL for download for the platforms listed in [Client versions & support policy](/release-notes/requirements).

## Related videos

> Snowflake 101 | SnowSQL

**Next Topics:**

- [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation)
- [Migrating from SnowSQL to Snowflake CLI](/user-guide/snowsql-migrate)
- [Installing SnowSQL](/user-guide/snowsql-install-config)
- [Configuring SnowSQL](/user-guide/snowsql-config)
- [Connecting through SnowSQL](/user-guide/snowsql-start)
- [Using SnowSQL](/user-guide/snowsql-use)
