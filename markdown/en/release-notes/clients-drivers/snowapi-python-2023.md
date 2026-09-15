# Snowflake Python APIs release notes for 2023

This article contains the release notes for the Snowflake Python APIs, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

See [Snowflake Python APIs: Managing Snowflake objects with Python](/developer-guide/snowflake-python-api/snowflake-python-overview) for documentation.

## Version 0.5.0 (2023-12-06)

### New features and updates

- Removed the experimental tags on all entities.

### Bug fixes

- Fixed a bug that raised an exception when listing databases and schemas.

## Version 0.4.0 (2023-12-04)

Initial public preview release.

### New features and updates

- Added support for Python 3.11.
- Updated the dependency on snowflake-snowpark-python to 1.5.0.
- Removed the Pydantic types from the model class.
- Renamed exception class names in `snowflake.core.exceptions`.

### Bug fixes

- Fixed a bug that raised an exception when listing some entities that have non-alphanumeric characters in the names.
