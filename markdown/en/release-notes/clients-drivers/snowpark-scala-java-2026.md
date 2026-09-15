# Snowpark Library for Scala and Java release notes for 2026

This article contains the release notes for
the [Snowpark Library for Scala](/developer-guide/snowpark/scala/index)
and [Snowpark Library for Java](/developer-guide/snowpark/java/index), including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowpark Library for Scala and Java updates.

See [Snowpark Developer Guide for Java](/developer-guide/snowpark/java/index) and [Snowpark Developer Guide for Scala](/developer-guide/snowpark/scala/index) for documentation.

## Version 1.20.0 (July 2, 2026)

### Bug Fixes

- Fixed escaping of string values containing single quotes and backslashes in column expressions, `substring_index`, and the `DataFrame.flatten` path argument so they are rendered correctly in generated SQL.
- Fixed integer literal SQL generation in `DataTypeMapper` so integer values are matched and cast correctly.

## Version 1.19.1 (May 27, 2026)

### Behavior changes

- Support for Scala 2.13 is now generally available starting with release 1.19.1. Scala 2.13 was previously in public preview beginning with release 1.17.0. For guidance on referencing the Snowpark package for each Scala version, see [Writing code to support different Scala versions](/developer-guide/scala-version-differences).

### Bug Fixes

- Fixed `LIST` SQL stage reference quoting by single-quoting stage references that contain non-ASCII characters.
- Fixed escaping of single quotes in `subfieldExpression` and `singleQuote` to prevent SQL injection.

## Version 1.19.0 (May 27, 2026)

### New features

Added the following new APIs:

- `functions.to_number`
- `functions.try_to_number`

### Improvements

- Added Java/Scala API support for user-defined aggregate functions (UDAFs).
- Added support for specifying `tableType` in `saveAsTable(...)`.

### Bug Fixes

- Fixed CTE query classification where CTE queries were not recognized as select queries.
- Fixed a `COPY INTO` SQL generation bug related to `stripMargin`.
- Fixed incorrect output from `Utils.normalizeStageLocation`.

## Version 1.16.2 (April 2, 2026)

### Bug Fixes

- Fixed a bug where `DataFrame.write.csv()` and `DataFrame.write.json()` would fail if the DataFrame created a query with the `|` character.

## Version 1.16.1 (March 19, 2026)

### Bug Fixes

- Fixed a bug where CTE queries could not run in async mode because they were not recognized as select queries.
