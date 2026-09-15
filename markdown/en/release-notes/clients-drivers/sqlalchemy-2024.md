# SQLAlchemy release notes for 2024

This article contains the release notes for the SQLAlchemy, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for SQLAlchemy updates.

See [Using the Snowflake SQLAlchemy toolkit with the Python Connector](/developer-guide/python-connector/sqlalchemy) for documentation.

## Version 1.7.2 (December 17, 2024)

### New features and updates

- Added support for structured `OBJECT` and `ARRAY` datatypes.

### Bug fixes

- Fixed an issue with quoting an underscore (`_`) as a column name.
- Fixed an issue with index columns not being reflected.
- Fixed an issue with the index reflection cache.

## Version 1.7.1 (December 02, 2024)

### New features and updates

- Added support for PARTITION BY to the COPY INTO command.

### Bug fixes

- Fixed the `BOOLEAN type not found` error in `snowdialect`.

## Version 1.7.0 (November 21, 2024)

### New features and updates

- Added support for the following features:

  - Dynamic Tables
  - Hybrid Tables
  - Iceberg Tables with the Snowflake Catalog
- Added support for the `MAP` data type.
- Added the ability to define options in key arguments instead of arguments.
- Updated the `cluster_by` option to support explicit expressions

### Bug fixes

- Fixed the `SAWarning` when registering functions with existing name in the default namespace.

## Version 1.6.1 (July 9, 2024)

### New features and updates

- None.

### Bug fixes

- Updated the internal project workflow with pypi publishing.

## Version 1.6.0 (July 8, 2024)

### New features and updates

- Added support for SQLAlchemy 2.0 syntax.

### Bug fixes

- None.

## Version 1.5.3 (April 16, 2024)

### New features and updates

- Limited the maximum SQLAlchemy dependency version to lower than 2.0.0.

### Bug fixes

- None.

## Version 1.5.2 (April 11, 2024)

### New features and updates

- Bumped the minimum SQLAlchemy version to 1.4.19 for Outer Lateral Joins.
- Added support for sequence ordering in tests.

### Bug fixes

- None.
