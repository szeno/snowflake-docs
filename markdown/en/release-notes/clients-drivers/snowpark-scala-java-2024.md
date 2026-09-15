# Snowpark Library for Scala and Java release notes for 2024

This article contains the release notes for
the [Snowpark Library for Scala](/developer-guide/snowpark/scala/index)
and [Snowpark Library for Java](/developer-guide/snowpark/java/index), including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowpark Library for Scala and Java updates.

See [Snowpark Developer Guide for Java](/developer-guide/snowpark/java/index) and [Snowpark Developer Guide for Scala](/developer-guide/snowpark/scala/index) for documentation.

## Version 1.15.0 (December 18, 2024)

Compatible Snowflake release: 8.46

### New features

- New functions:

  - `months_between`
  - `instr`
  - `format_number`
  - `from_unix_timestamp`
  - `to_unix_timestamp`
  - `Row.getAs`
- Support for SQL bind in `Session.sql` function.

## Version 1.14.0 (September 4, 2024)

Compatible Snowflake release: 8.35

### New features

- Added support for reading structured types from Snowflake.
- Added the following new functions:
  - `Variant.asJsonNode`
  - `Functions.round`
  - `Functions.hex`
  - `Functions.unhex`
  - `Functions.shiftleft`
  - `Functions.shiftright`
  - `Functions.reverse`
  - `Functions.isnull`
  - `Functions.unix_timestamp`
  - `Functions.locate`
  - `Functions.ntile`
  - `Functions.radn`
  - `Functions.randn`
  - `Functions.regexp_extract`
  - `Functions.signum`
  - `Functions.sign`
  - `Functions.substring_index`
  - `Functions.collect_list`
  - `Functions.log10`
  - `Functions.log1p`
  - `Functions.base64`
  - `Functions.unbase64`
  - `Functions.expr`
  - `Functions.array`
  - `Functions.date_format`
  - `Functions.last`
  - `Functions.desc`
  - `Functions.asc`
  - `Functions.size`

### Improvements

None.

### Bug fixes

- Fixed incorrect time info in the Open Telemetry span
- Fix duplicated Open Telemetry span in the count action

## Version 1.13.2 (August 26, 2024)

Compatible Snowflake release: 8.31

### New features

None.

### Improvements

None.

### Bug fixes

- Fixed Jackson Scala module compatibility issue.

## Version 1.13.1 (August 21, 2024)

Compatible Snowflake release: 8.31

### New features

None.

### Improvements

None.

### Bug fixes

- When the session parameter `ERROR_ON_NONDETERMINISTIC_UPDATE` is set to `true`, calls to `session.table(...).update(...)`
  no longer report errors.

## Version 1.13.0 (August 1, 2024)

Compatible Snowflake release: 8.28

### New features

- Emit span in Java/Scala stored procedure. Support functions:

  - All action functions
  - Register UDF/UDTF/SProc
- Enable retrieving cloud provider tokens in the `SnowflakeSecrets` class.
- New functions:

  - `Session.updateQueryTag`
  - `functions.countDistinct`
  - `functions.max(String)`
  - `functions.min(String)`
  - `functions.mean(String)`

### Improvements

- App name in the session query tag is JSON format now.
- Upgraded SLF4J to 2.0.4
- Update documentation for `SnowflakeFile`

### Bug fixes

- Variant object can’t handle null value
- `DataFrame` alias doesn’t work in the JOIN condition

## Version 1.12.1 (May 13, 2024)

Compatible Snowflake release: 8.18

### New features

None.

### Improvements

None.

### Bug fixes

Fixed “Dataframe alias doesn’t work in the JOIN condition”.

## Version 1.12.0 (April 16, 2024)

Compatible Snowflake release: 8.14

### New features

- Support the `Geometry` data type.
- New function: `sum(String)`.
- Support setting an app name when creating a new session.

### Improvements

Added code examples for the `split` function in the API document.

### Bug fixes

None.

## Version 1.11.0 (April 1, 2024)

Compatible Snowflake release: 8.12

### New features

- Support Java 17 stored procedure
  - When registering a stored procedure, Snowpark automatically sets `runtime_version` to 17 if the client is running with JVM 17.

### Improvements

None.

### Bug fixes

None.

## Version 1.10.0 (February 9, 2024)

Compatible Snowflake release: 8.5

### New features

- Support Java 17.

  - Compatible with JVM 17.
  - When registering a UDF or UDTF, Snowpark automatically sets the `runtime_version` to `17` if the client is running with
    JVM 17.
- Support Dataframe alias.

  - You can use the `DataFrame.alias` function to assign DataFrames an alias for future reference.

    For example, you could use code such as the following:

    Copy code

    ```
    val df1 = df.alias("A")
    df1.join(df2).select(col("A.col"))
    ```

    This is equivalent to `df1.join(df2).select(df1("col"))`.
- Support for the `explode` function.
- You can invoke table functions in the `DataFrame.select` method.
- You can use table functions to read function arguments through the `TableFunction.apply` method.
- New session constructor `Session.getOrCreate`.

### Improvements

- Upgraded JDBC to version 3.14.4.
- New wrapper for `is_null` function.
- Upgrade Scala to version 2.12.18.

### Bug fixes

- Updated wrong license information.
