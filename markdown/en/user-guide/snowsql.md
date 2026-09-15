# SnowSQL (CLI client)

Note

[Snowflake CLI](/developer-guide/snowflake-cli/index) is an open-source command-line tool explicitly designed for developer-centric workloads in addition to SQL operations. Snowflake CLI is a more modern, robust, and efficient CLI client than legacy SnowSQL. Snowflake CLI not only lets you execute SQL commands, but also lets you execute commands for other Snowflake products like Streamlit in Snowflake, Snowpark Container Services, and Snowflake Native App Framework. Snowflake will only add new features and enhancements to Snowflake CLI. Consequently, Snowflake recommends that you begin transitioning from SnowSQL to Snowflake CLI.

To help you with the transition from SnowSQL to Snowflake CLI, see [Migrating from SnowSQL to Snowflake CLI](/user-guide/snowsql-migrate).

As of July 2025, Snowflake will provide support based on the minor releases for SnowSQL, as follows:

> | SnowSQL version | Initial release date | Support end date |
> | --- | --- | --- |
> | 1.2.x | February 02, 2023 | December 19, 2025 |
> | 1.3.x | May 02, 2024 | May 02, 2026 |
> | 1.4.x | May 22, 2025 | May 22, 2027 |
> | 1.5.x | April 16, 2026 | April 16, 2028 |
>
> Expand
>
> Show lessSee more

SnowSQL is a legacy command-line client for connecting to Snowflake to execute SQL queries and perform all DDL and DML operations, including loading data into and unloading data out of database tables.

SnowSQL (`snowsql` executable) can be run as an interactive shell or in batch mode through `stdin` or using the `-f` option.

SnowSQL is an example of an application developed using the [Snowflake Connector for Python](/developer-guide/python-connector/python-connector); however, the connector is not a prerequisite for installing SnowSQL. All required software for installing SnowSQL
is bundled in the installers.

Snowflake provides platform-specific versions of SnowSQL for download for the platforms listed in [Client versions & support policy](/release-notes/requirements).

## Related videos

> Snowflake 101 | SnowSQL

**Next Topics:**

- [Installing SnowSQL](/user-guide/snowsql-install-config)
- [Configuring SnowSQL](/user-guide/snowsql-config)
- [Connecting through SnowSQL](/user-guide/snowsql-start)
- [Using SnowSQL](/user-guide/snowsql-use)
