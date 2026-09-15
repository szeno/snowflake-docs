# Ingest Java SDK release notes for 2023

This article contains the release notes for the Ingest Java SDK, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Ingest Java SDK updates.

## Version 2.0.4 (October 31, 2023)

### New features and updates

- Supported a new ON\_ERROR option SKIP\_BATCH, which skips the entire batch if there is any issue and returns all errors as part of the response.
- Added row index information to all exceptions.
- Upgraded snappy-java dependency.
- Added a new interface to return the table schema information for a channel.
- Added a new configuration option MAX\_CLIENT\_LAG that specifies the flush frequency, in seconds (default: 1).

### Bug fixes

- Fixed an issue with using `snowflake-jdbc-fips`.
- Fixed a rare `ConcurrentModificationException` issue.
- Fixed two issues in `insertRows` API that might cause wrong results in a very rare case.
- Limited the maximum allowed number of chunks in blob to avoid the case when the request is too large.

## Version 2.0.3 (August 31, 2023)

### New features and updates

- Supported OAuth authentication.
- Removed exactly-once related code for Snowpipe.
- Supported publishing unshaded snapshot release to the Nexus repo.
- Added retry logic for invalid JWT tokens.
- Added a warning for large batches in `insertRows`.

### Bug fixes

- Fixed a NPE issue caused by race condition.

## Version 2.0.2 (July 25, 2023)

### New features and updates

- Updated dependencies based on Wiz and Snyk vulnerability scan results.
- Improved retry logic on exceptions like `SSLException`.
- Made the role as an optional input and supported using the default role associated with the user.
- Sent uncompressed chunk lengths to server side for tracking purpose.

### Bug fixes

- None.

## Version 2.0.1 (June 14, 2023)

### New features and updates

- None.

### Bug fixes

- Fixed an unexpected dependency behavior for Snowflake JDBC.

## Version 2.0.0 (June 13, 2023)

### New features and updates

- Supported Snowpipe Streaming GA release.
- Improved the dependencies for shading and relocating logic.
- Made a few parameters to configure channel/chunk/file size limits.
- Added more telemetries to track end-to-end latency.
- Supported GCS downscoped token.
- Cleaned up all Arrow related code.
- Added an attribution notice.
- Enforced allowed DATE and TIMESTAMP range.
- Exposed more error messages for server-side channel invalidation for customers to self-mitigate.

### Bug fixes

- Fixed an issue where some background threads are not stopped during exception.
