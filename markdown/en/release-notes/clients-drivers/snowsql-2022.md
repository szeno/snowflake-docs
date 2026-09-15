# SnowSQL release notes for 2022

This article contains the release notes for the SnowSQL, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for SnowSQL updates.

See [SnowSQL (CLI client)](/user-guide/snowsql) for documentation.

## Version 1.2.24 (October 21, 2022)

### New Features

- Fixed an issue where a StopIteration exception was raised while using a TAB to complete a command.

## Version 1.2.23 (July 28, 2022)

### Bug Fixes

- Reverted to the legacy SQL splitter implementation as the default, as the new splitter implementation led to
  unforeseen behavior changes.

## Version 1.2.22 (June 29, 2022)

### New Features

- SnowSQL now captures proxies set by environment variables in logs.

### Bug Fixes

- Fixed an issue where SnowSQL returned Unicode characters as escape sequences instead of the actual Unicode characters.
- Removed the deprecation warning when using proxy variables.
