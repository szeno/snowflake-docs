# Snowpark Library for Scala and Java release notes for 2025

This article contains the release notes for
the [Snowpark Library for Scala](/developer-guide/snowpark/scala/index)
and [Snowpark Library for Java](/developer-guide/snowpark/java/index), including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowpark Library for Scala and Java updates.

See [Snowpark Developer Guide for Java](/developer-guide/snowpark/java/index) and [Snowpark Developer Guide for Scala](/developer-guide/snowpark/scala/index) for documentation.

## Version 1.18.0 (December 5, 2025)

### Improvements

- Add `functions.try_to_date` overload for format parameter.
- Add `functions.try_to_timestamp` overload for format parameter.
- Add `Column.cast` support for `Any` parameter type.
- Add `Column.equal_to` support for `Any` parameter type.
- Add `Column.not_equal` support for `Any` parameter type.
- Add `Column.gt` support for `Any` parameter type.
- Add `Column.lt` support for `Any` parameter type.
- Add `Column.leq` support for `Any` parameter type.
- Add `Column.geq` support for `Any` parameter type.
- Add `Column.equal_null` support for `Any` parameter type.
- Add `Column.plus` support for `Any` parameter type.
- Add `Column.minus` support for `Any` parameter type.
- Add `Column.multiply` support for `Any` parameter type.
- Add `Column.divide` support for `Any` parameter type.
- Add `Column.mod` support for `Any` parameter type.

## Version 1.17.0 (November 10, 2025)

Compatible Snowflake release: 9.32

### New features

Added the following new APIs:

- `DataFrame.isEmpty`
- `functions.try_to_timestamp`
- `functions.try_to_date`
- `functions.concat_ws_ignore_nulls`
- `functions.array_flatten`
- `Row.mkString` (with overloads for customizable separators and formatting options)
- `StructType.fieldNames` (alias for `StructType.names`)

### Improvements

- Support both Scala 2.12 and 2.13 (currently in public preview) from release 1.17.0 onwards.
- `functions.when` and `Column.when`, along with `Column.otherwise`, now accept any literal arguments (for example, `String`, `int`, `boolean`, or `null`) in addition to `Column` instances.
- Add `functions.substring` overload with support for start position and length arguments.
- Add `functions.lpad` overloads to pad with `String`, or `Array[Byte]`.
- Add `functions.rpad` overloads to pad with `String`, or `Array[Byte]`.
- Add `DataFrame.sort` overload with support for variadic arguments.
- Add `DataFrame.show` overloads with parameters to control truncation and number of displayed rows.

### Bug Fixes

None.

## Version 1.16.0 (June 30, 2025)

Compatible Snowflake release: 9.17

### New features

None.

### Improvements

- Upgraded Snowflake JDBC to 3.24.2.
- Added support for empty input `Seq` in `Column.in`.
- Added support for creating views from `Union` results.

### Bug Fixes

- Fixed a wrong order issue when merging a Dataframe.
