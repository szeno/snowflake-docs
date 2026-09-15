# Snowflake Connector for Spark release notes for 2023

This article contains the release notes for the Snowflake Connector for Spark, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Spark updates.

See [Snowflake Connector for Spark](/user-guide/spark-connector) for documentation.

## Version 2.12.0 (May 23, 2023)

Note

Starting with this version (2.12.0), the Snowflake Connector for Spark no longer supports Spark 3.1, but continues to support versions 3.2, 3.3, and 3.4. Previous versions of the connector continue to support Spark 3.1.

### New features

- Added support for Spark 3.4.
- Built and tested with the Snowflake JDBC driver, version 3.13.30.

### Bug fixes

- None.

## Version 2.11.3 (April 21, 2023)

### New features

- Updated the mechanism for writing DataFrames to accounts on GCP. After December 2023, previous versions of the Spark Connector will no longer be able to write DataFrames, due to changes in GCP.
- Added the option to disable `preactions` and `postactions` validation for session sharing.

  To disable validation, set the option `FORCE_SKIP_PRE_POST_ACTION_CHECK_FOR_SHARED_SESSION` to `true`. The default is `false`.

  Important

  Before setting this option, make sure that the queries in `preactions` and `postactions` don’t affect the session settings. Otherwise, you might encounter issues with results.

### Bug fixes

- Fixed an issue when performing a join or union across different schemas when the two DataFrames are accessing
- tables with different `sfSchema` and the same name table in `sfSchema` is in the left `DataFrame`.

## Version 2.11.2 (March 21, 2023)

### New features

- Added support for sharing a JDBC connection.

  The Snowflake Connector for Spark can now use the same JDBC connection for different jobs and actions when the
  client uses the same connection options to access Snowflake. Previously, the Spark Connector created a new
  JDBC connection for each job or action.

  The Spark Connector supports the following options and API methods for enabling and disabling this feature:

  - To specify that the connector should not use the same JDBC connection, set the `support_share_connection` connector
    option to `false`. (The default value is `true`, which means that the feature is enabled.)
  - To enable or disable the feature programmatically, call one of the following global static functions:
    `SparkConnectorContext.disableSharedConnection()` and `SparkConnectorContext.enableSharingJDBCConnection()`.

  Note

  In the following special cases, the Spark Connector will not use the shared connection:

  - If `preactions` or `postactions` are set, and those `preactions` or `postactions` are not CREATE TABLE,
    DROP TABLE, or MERGE INTO, the Spark Connector will not use the shared connection.
  - Utility functions in `Utils`, such as `Utils.runQuery()` and `Utils.getJDBCConnection()`, will not use the
    shared connection.
- Updated the connector to use the Snowflake JDBC driver 3.13.29.

### Bug fixes

- None.
