# .NET Driver release notes for 2022

This article contains the release notes for the .NET Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for .NET Driver updates.

See [.NET Driver](/developer-guide/dotnet/dotnet-driver) for documentation.

## Version 2.0.19 (November 16, 2022)

### New features

- Updated the `System.Text.RegularExpressions` library to version 4.3.1.

## Version 2.0.18 (November 02, 2022)

### BCR (Behavior Change Release) change

Caution

Version 2.0.18 of the Snowflake .NET driver changed the way it handles escaping the equal sign (=) in
connection strings to match the .NET specification. Specifically, if a password contained an equal sign, you had to
escape the character by using double equal signs (==). If your projects are affected by breaking changes related
specifically to special characters, Snowflake recommends that you do not install this version into a production
environment before testing.

### New features

- Improved PUT and GET command queries:
- Query strings are case-insensitive.
- White space is allowed at the start and end of query strings.
- White space is permitted in file paths for PUT queries.
- Added the `CLIENT_SESSION_KEEP_ALIVE` configuration property to prevent a session from timing out.
- Added ability to execute a batch of SQL statements (multi-statement support).
- Added support for connecting to proxy servers.

### Bug fixes

- Changed special character handling in connection strings to match the Microsoft .NET specifications.

## Version 2.0.17 (October 3, 2022)

### Bug fixes

- Added the `SetPooling()` function to enable and disable connection pooling.

## Version 2.0.16 (August 24, 2022)

### Behavior Change Release (BCR) change

Caution

Version 2.0.16 of the Snowflake .NET driver includes an update that replaces targeting .NET Standard 2.0
with .NET 6.0. If your projects are affected by breaking changes related specifically to .NET 6.0, you must update your
framework or project to use the new version. Snowflake recommends that you do not install this version into a
production environment before testing.

### Bug fixes

- Fixed an issue where unicode characters appended an extra “u” for large streams (e.g “/u007f” becomes “/u007fu”).

## Version 2.0.15 (July 19, 2022)

### Bug fixes

- Updated the exception thrown for incorrect private key.

## Version 2.0.14 (June 23, 2022)

### New features

- Updated `SnowflakeDbException.ToString` to include more error details.
- Added support for bulk array binding.
- Added support for connection pools.

## Version 2.0.13 (May 18, 2022)

### New features

- Added option to disable automatically retrying to connect when a connection fails or drops.
- Added byte encryption bytes to read and write chunks for the PUT command.

### Bug fixes

- Resolved an issue where DEL characters displayed incorrectly.

## Version 2.0.12 (May 06, 2022)

### New Feature

- Added support for the GET command.

## Version 2.0.11 (Mar 15, 2022)

### New Feature

- Added support for the PUT command.

## Version 2.0.10 (Feb 16, 2022)

### Bug fixes

- Resolved issues with asynchronous warning messages returned by the Snowflake ChunkDownloader.

## Version 2.0.9 / 1.2.9 (Jan 18, 2022)

### Bug fixes

- Fixed an issue with external browser authentication on non-Windows platforms.
- Returned `TIMESTAMP` values now defaults to `DateTimeKind.Unspecified` instead of DateTimeKind.Utc
- Made the chunk downloader’s parser run asynchronously.
