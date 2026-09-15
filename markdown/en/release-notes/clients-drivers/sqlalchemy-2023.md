# SQLAlchemy release notes for 2023

This article contains the release notes for the SQLAlchemy, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for SQLAlchemy updates.

See [Using the Snowflake SQLAlchemy toolkit with the Python Connector](/developer-guide/python-connector/sqlalchemy) for documentation.

## Version 1.5.1 (November 2, 2023)

### New features and updates

- None.

### Bug fixes

- Fixed a compatibility issue with restrictions on outer lateral joins. For more details check [Table Functions (Except SQL UDTFs): Restrictions With Lateral Table Functions and Outer Lateral Joins](/release-notes/bcr-bundles/2023_04/bcr-1057).
- Fixed credentials with externalbrowser authentication not caching due to incorrect parsing of Boolean query parameters, as well as other Boolean parameters passed to the driver.

## Version 1.5.0 (August 24, 2023)

### New features and updates

- Added support for the `GEOMETRY` data type.

### Bug fixes

- Fixed a compatibility issue with standard SQLAlchemy 1.4.49 library.

## Version 1.4.7 (March 21, 2023)

### New features and updates

- `SnowflakeDialect.get_columns` now throws a `NoSuchTableError` exception when the specified table doesn’t exist,
  instead of the more vague `KeyError`.
- Fixed a bug where dialect can not be created with empty host name.
- Fixed a bug where `sqlalchemy.func.now` did not render correctly.

### Bug fixes

- None.

## Version 1.4.6 (February 8, 2023)

### New features and updates

- Bumped the `snowflake-connector-python` dependency to newest version, which supports Python 3.11.
- Reverted the change of application name introduced in version 1.4.5 until the feature is supported.

### Bug fixes

None.
