# SQLAlchemy release notes for 2022

This article contains the release notes for the SQLAlchemy, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for SQLAlchemy updates.

See [Using the Snowflake SQLAlchemy toolkit with the Python Connector](/developer-guide/python-connector/sqlalchemy) for documentation.

## Version 1.4.5 (December 9, 2022)

### New features

- Updated the application name for the driver connection from SnowflakeConnection to SnowflakeSQLAlchemy.

## Version 1.4.4 (November 16, 2022)

### Bug Fixes

- Fixed a bug where percent signs (%) in a non-compiled statement should not be interpolated with empty sequence
  when executed.

## Version 1.4.3 (October 21, 2022)

### Bug fixes

- Fixed an issue `whereSnowflakeDialect.normalize_name` and `SnowflakeDialect.denormalize_name` could not handle
  empty strings.
- Fixed a compatibility issue to vendor function `sqlalchemy.engine.url._rfc_1738_quote` as it is removed from
  SQLAlchemy v1.4.42.

## Version 1.4.2 (September 28, 2022)

### Updates

- Improved reliability by always using context managers.

## Version 1.4.1 (August 23, 2022)

### Updates

- None.

### Bug Fixes

- Fixed an issue where DATE was incorrectly removed from `SnowflakeDialect.ischema_names`.
- Fixed breaking changes introduced in release 1.4.0 that:
  - Changed the behavior of processing numeric, datetime, and timestamp values returned from service.
  - Changed the sequence order of primary/foreign keys in list returned by `inspect.get_foreign_keys`
    and `inspect.get_pk_constraint`.

## Version 1.4.0 (July 21, 2022)

### New Features

- Added support for `regexp_match` and `regexp_replace` in `sqlalchemy.sql.expression.ColumnOperators`.
- Added support for Identity Column.
- Added support for handling literal values for the sql types: `Date`, `DateTime`, `Time`, `Float`, and `Numeric`;
  also added support for converting the values into corresponding Python objects.
- Added support for `get_sequence_names` in `SnowflakeDialect`.

### Bug Fixes

- Fixed a bug where insert with `autoincrement` failed due to incompatible column type affinity.
- Fixed a bug when creating a column with sequence, default value was set incorrectly.
- Fixed a bug that identifier having percents in a compiled statement was not interpolated.
- Fixed a bug when visiting sequence value from another schema, the sequence name is not formatted with the schema name.
- Fixed a bug where the sequence order of columns were not maintained when retrieving primary keys and foreign
  keys for a table.
