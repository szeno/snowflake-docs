# Snowflake Connector for Spark release notes for 2024

This article contains the release notes for the Snowflake Connector for Spark, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Spark updates.

See [Snowflake Connector for Spark](/user-guide/spark-connector) for documentation.

## Version 3.0.0 (July 31, 2024)

### BCR (Behavior Change Release) changes

Beginning with version 3.0.0, the Snowflake Connector for Spark introduced the following breaking changes:

- Removed the Advanced Query Pushdown feature.

  Alternatives to the feature are available. For example, instead of loading data from Snowflake tables, users can directly load data from Snowflake SQL queries.

  Snowflake plans to introduce a tool to convert DataFrames between Spark and Snowpark in a future Snowflake Connector for Spark release.
- Each release now includes one artifact instead of multiple artifacts for different Spark versions.

  The single artifact works with multiple Spark versions. Currently, Snowflake verified support for Spark 3.4 and 3.5 in the Snowflake Connector for Spark 3.0.0 version.

Per Snowflake’s support policy, Snowflake will continue to support Spark 2.x.x versions for up to two years.

### New features

- Upgraded JDBC to 3.17.0 to Support LOB.
- Added support for Spark 3.5.0.

### Bug fixes

- Removed the requirement of the `SFUSER` parameter when using OAUTH.

## Version 2.16.0 (June 10, 2024)

### New features

- Upgraded JDBC to version 3.16.1.
- Improved legacy Spark streaming code.
- Disabled the `abort_detached_query` parameter at the session level by default.

### Bug fixes

- Fixed an issue with the proxy protocol that incorrectly impacted S3 protocols.

## Version 2.15.0 (February 26, 2024)

### New features

- Introduced a new `trim_space` parameter that you can use to trim values of `StringType` columns automatically when saving to a Snowflake table. Default: `false`.

### Bug fixes

- Fixed an issue that caused a “cancelled queries can be restarted in the Spark retries after application closed” message.
