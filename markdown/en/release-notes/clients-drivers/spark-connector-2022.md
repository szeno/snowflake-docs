# Snowflake Connector for Spark release notes for 2022

This article contains the release notes for the Snowflake Connector for Spark, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Spark updates.

See [Snowflake Connector for Spark](/user-guide/spark-connector) for documentation.

## Version 2.11.1 (December 13, 2022)

### New features

- Added support for AWS VPCE deployments by adding the S3\_STAGE\_VPCE\_DNS\_NAME configuration parameter to specify the
  VPCE DNS name at the session level.
- Added a new configuration option treat\_decimal\_as\_long to enable the Spark Connector to return Long values
  instead of `BigDecimal` values, if the query returns `Decimal(<any_precision>, 0)`. WARNING: If the value is
  greater than the maximum value of `Long`, an error will be raised.
- Added a new option proxy\_protocol for specifying the proxy protocol (http or https) with AWS deployments.
  (The option has no effect on Azure and GCP deployments.).
- Added support for counting rows in a table where the row count is greater than the maximum value of Integer.
- Updated the connector to use the Snowflake JDBC driver 3.13.24.

### Bug fixes

- Updated the connector to close JDBC connections to avoid connection leakage.
- Fixed a `NullPointerException` issue when sending telemetry messages.

## Version 2.11.0 (September 2, 2022)

Compatible JDBC Driver version: 3.13.22

- Added support for Spark 3.3 and fixed some bugs:
  - Upgraded the version of the PostgreSQL JDBC Driver that tests depend on to avoid the security
    vulnerability [CVE-2022-31197](https://github.com/advisories/GHSA-r38f-c4h4-hqq2).
  - Updated the connector to use the Snowflake JDBC driver 3.13.22 and the Snowflake Ingest SDK 0.10.8.

Note

- Starting from version 2.11.0, the Snowflake Connector for Spark supports Spark 3.1, 3.2 and 3.3.
  Version 2.11.0 of the Snowflake Connector for Spark does not support Spark 3.0. Note that previous versions of the connector continue to support Spark 3.0.
- For Snowflake GCP accounts, the Snowflake JDBC driver versions 3.13.16 through 3.13.21 do not work with the Spark connector.

## Version 2.10.1 (August 15, 2022)

Compatible JDBC Driver version: 3.13.14

### Bug fixes

- Removed unnecessary dependencies on libraries to avoid the security vulnerabilities
  [CVE-2020-8908](https://github.com/advisories/GHSA-5mg8-w23w-74h3) and [CVE-2018-10237](https://github.com/advisories/GHSA-mvr2-9pj6-7w5j).
- Added support for using the JDBC data type `TIMESTAMP_WITH_TIMEZONE` when reading data from Snowflake.
- Changed the logic for checking for the existence of a table before saving a DataFrame to Snowflake:

  - The connector now reuses the existing connection (rather than creating a new connection) to avoid potential problems with token expiration.
  - If the table name is not fully qualified (i.e. does not include the schema name), the connector now checks for the table under the schema specified by sfSchema, rather than the schema that is currently in use in the session.

    Note

    If you need to save a DataFrame to a table in a schema other than `sfSchema`, specify the schema as part of
    the fully qualified name of the table, rather than executing USE SCHEMA to change the current schema.
- Improved performance by avoiding unnecessary `parse_json()` calls in the COPY INTO TABLE command when writing a
  DataFrame with `ArrayType`, `MapType`, or `StructType` columns to Snowflake.
- Added the `getLastSelectQueryId` and `getLastCopyLoadQueryId` methods to the `Utils` class. These methods
  return the query ID of the last query that read data from Snowflake and the last COPY INTO TABLE statement that
  was executed (respectively).

## Version 2.10.0 (February 17, 2022)

Compatible JDBC Driver version: 3.13.14

### Behavior change

- Added support for Spark, version 3.2. Beginning with this release, the Snowflake Connector for Spark only supports Spark 3.0, 3.1 and 3.2. Spark version 2.4 is no longer supported.

### Bug fix

- Fixed an issue where string “null” is regarded as type `NULL`.
