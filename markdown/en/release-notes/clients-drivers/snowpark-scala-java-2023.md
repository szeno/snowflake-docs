# Snowpark Library for Scala and Java release notes for 2023

This article contains the release notes for
the [Snowpark Library for Scala](/developer-guide/snowpark/scala/index)
and [Snowpark Library for Java](/developer-guide/snowpark/java/index), including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowpark Library for Scala and Java updates.

See [Snowpark Developer Guide for Java](/developer-guide/snowpark/java/index) and [Snowpark Developer Guide for Scala](/developer-guide/snowpark/scala/index) for documentation.

## Version 1.9.0 (October 17, 2023)

Compatible Snowflake release: 7.36

### New features

- Supports `regexp_replace` function.
- Supports `PKCS#8` RSA private key.

### Improvements

- Upgraded Snowflake JDBC to 3.14.1.

### Bug fixes

- None.

## Version 1.8.0 (April 28, 2023)

Compatible Snowflake release: 7.14

### New features

- New APIs for creating and calling stored procedures.

  This release includes APIs for registering named permanent, named session-temporary, and anonymous session-temporary stored procedures. It also includes APIs for calling stored procedures, both registered in Snowflake and to run locally.

  For related APIs, refer to the following.

  - For Java: [com.snowflake.snowpark\_java.SProcRegistration](https://docs.snowflake.com/developer-guide/snowpark/reference/java/com/snowflake/snowpark_java/SProcRegistration.html)
  - For Scala: [com.snowflake.snowpark.SProcRegistration](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/SProcRegistration.html)
- `Session.tableFunction` function now also works with `DataFrame` columns.

  Previously, the `Session.tableFunction` method only supported literal function arguments. With this release, you can
  specify `DataFrame` columns from a single frame as an argument. For more information, refer
  to [tableFunction](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/Session.html#tableFunction(func:com.snowflake.snowpark.TableFunction,args:Seq%5Bcom.snowflake.snowpark.Column%5D):com.snowflake.snowpark.DataFrame)
  in the reference documentation.

  Note that all `DataFrame` columns used as arguments should come from the same `DataFrame`.

### Improvements

- Upgraded the Snowflake JDBC driver to 3.13.28.

### Bug fixes

- None.

## Version 1.7.2 (February 16, 2023)

Compatible Snowflake release: 7.13

### New features

- None.

### Improvements

- Updated `SnowflakeFile` class to the latest version.

### Bug fixes

- None.

## Version 1.7.1 (February 8, 2023)

Compatible Snowflake release: 7.6.x

### New features and Updates

- Improved an internal feature for stored procedure support.
- Updated the `SnowflakeFile` class to the latest version.

### Bug fixes

- None.

## Version 1.7.0 (January 7, 2023)

Compatible Snowflake release: 7.0.x

### New features

- Added methods that support PARTITION BY and ORDER By when joining a DataFrame with the output of a UDTF.

### Improvements

- Made more predictable the result when column heads are duplicated across joined DataFrames.
  As of this release, duplicated column names will be presented as found in the DataFrames that were joined.
  Previously, aliases were used for duplicated column heads. Aliases will still be used for duplicated column
  heads when the result of a join is saved to a table or cached – you should deduplicate before saving or caching.

### Behavior changes

- Changed from `int` to `long` the return value data type of methods that return a count of rows merged, updated, or
  deleted. For these methods, see the `MergeResult`, `UpdateResult`, and `DeleteResult` types.
