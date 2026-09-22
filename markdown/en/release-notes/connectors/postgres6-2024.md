# Snowflake Connector for PostgreSQL release notes for 2024

This topic provides release notes for the Snowflake Connector for PostgreSQL.
For additional information, see [Snowflake connector for PostgreSQL](https://other-docs.snowflake.com/en/connectors/postgres6/about).

## Version 6.9.1 (December 12th, 2024)

### Behavior changes

- The native application has been migrated to the new [event-sharing model](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging). Telemetry sharing is now mandatory for all event types, such as logs and traces, and it can’t be disabled for the new installations. For already existing installations, you will receive an email with our account locator “EOA66985” asking you to review and configure the required event sharing.

### New features

- The connector supports column types that are not listed in the pg\_type table.

### Bug fixes

- Stopped printing the warning in the agent: “JAXB is unavailable. Will fallback to SDK implementation which may be less performant”.
- Stopped printing the warning in the agent: “Unable to load native-hadoop library for your platform… using builtin-java classes where applicable”.

## Version 6.8.0 (November 22nd, 2024)

### Behavior changes

- Increased the minimum schedule interval to 15 minutes.

  Pre-existing 10-minute intervals remain unchanged. Snowflake recommends setting them to at least 15 minutes.
- The operational warehouse will now suspend when there is no data traffic from the source database for more than 5 minutes.
- The `Killing agent on shutdown container` error message will not show when triggering the agent’s shutdown. Instead, the following message will be logged on the INFO level: `Stopping the agent on the container shutdown signal`.

### New features

- The *PUBLIC.REMOVE\_TABLES(DATA\_SOURCE\_NAME STRING, SCHEMA\_NAME STRING, TABLE\_NAMES ARRAY)* procedure enables the removal of multiple tables with one call.

### Bug fixes

- The operational warehouse will now correctly suspend when all data sources are switched to a scheduled mode.
- The agent will no longer restart when the logging rate is too high.
- Fixed failing table replication on PostgreSQL numerics *NaN*, *Infinity*, *-Infinity* by ingesting them as *null*.
- Fixed replication errors when the *DEFAULT\_DDL\_COLLATION* parameter for account is set.

## Version 6.6.1 (October 3rd, 2024)

### Behavior changes

- The maximum connection pool size to source databases has been increased to 7.

### New features

Not applicable.

### Bug fixes

- The agent no longer stops after encountering data source connectivity issues.
- The agent now confirms the PostgreSQL WAL position even when the `QUOTED_IDENTIFIERS_IGNORE_CASE` parameter is enabled for an account.

## Version 6.6.0 (September 17th, 2024)

### Behavior changes

Not applicable.

### New features

- You can now configure the agent through environment properties in addition to using `snowflake.json` and `datasources.json` for configuration.
- You can now pass the private key contents through the `snowflake.private-key` property or `SNOWFLAKE_PRIVATEKEY` environment variable.

For more information, see [Configure and run the agent](https://other-docs.snowflake.com/en/connectors/postgres6/install-agent#configure-and-run-the-agent).

### Bug fixes

- When schema introspection fails the operational warehouse suspends in the scheduled mode.
- Fixed a bug where some commands to stop table replication were ignored in a few cases.
- Fixed a bug where some source tables couldn’t be added to the replication and returned the error message `Tables are not ready to be re-added`.

## Version 6.5.0 (August 27th, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- In continuous mode, the compute warehouse will now be able to suspend if there is no data to merge into destination tables.

## Version 6.4.0 (August 16th, 2024)

### Behavior changes

- The connector now supports all known types of Postgres publications.

### New features

- Added support for all PostgreSQL DOMAIN types based on native data types.

### Bug fixes

- Corrected an issue where the connector could become stuck in a state where commands were not delivered to the agent.

## Version 6.3.2 (July 15th, 2024)

Initial release of version 6.3.2.

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed handling of deleted columns in subsequent schema changes.
- Fixed compute warehouse not suspending in scheduled mode.
- Fixed validation of reserved column names to be case insensitive.
- Fixed MySQL tables failing replication on huge transactions.

## Version 6.3.0 (July 11th, 2024)

Initial release of version 6.3.0.

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

Not applicable.
