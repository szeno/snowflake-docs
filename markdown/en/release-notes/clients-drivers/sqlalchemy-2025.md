# SQLAlchemy release notes for 2025

This article contains the release notes for the SQLAlchemy, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for SQLAlchemy updates.

See [Using the Snowflake SQLAlchemy toolkit with the Python Connector](/developer-guide/python-connector/sqlalchemy) for documentation.

## Version 1.8.2 (December 10, 2025)

### New features and updates

- None.

### Bug fixes

- Aligned the supported maximum python version with snowflake-connector-python to 3.13.

## Version 1.8.0 (December 04, 2025)

### New features and updates

- Added logging of the SQLAlchemy version and pandas (if used).
- Added support for Python 3.14 and earlier.

### Bug fixes

- None.

## Version 1.7.7 (Sep 09, 2025)

### New features and updates

- None.

### Bug fixes

- Fixed an issue that threw an exception for structured type columns dropped while collecting metadata.

## Version 1.7.6 (July 10, 2025)

### New features and updates

- None.

### Bug fixes

- Fixed an issue with `get_multi_indexes` that assigned the wrong returned indexes when processing multiple indexes in a table.

## Version 1.7.4 (June 10, 2025)

### New features and updates

- Updated `README.md` to include instructions on how to verify package signatures using cosign.

### Bug fixes

- Fixed a dependency on DESCRIBE TABLE columns quantity (differences in columns caused by Snowflake parameters).
- Fixed an unnecessary condition that caused issues when parsing `StructuredTypes` columns.

## Version 1.7.3 (January 14, 2025)

### New features and updates

- Added the `force_div_is_floordiv` flag to override the new default value (`False`) for `div_is_floor_div` in `SnowflakeDialect`.
  - When `force_div_is_floordiv` is `False`, the division (`/`) operator is treated as a float division, while the `//` operator is treated as floor division.
  - This flag is added to maintain backward compatibility with the previous `SnowflakeDialect` behavior.
  - This flag will be removed in a future release, and `SnowflakeDialect` will use `div_is_floor_div` as `False`.

### Bug fixes

- Fixed an issue with support for the SqlAlchemy ARRAY,
- Fixed the return value of `snowflake get_table_names`.
- Fixed incorrect quoting of identifiers beginning with an underscore (`_`).
- Fixed the “ARRAY type not supported in HYBRID tables” error.
