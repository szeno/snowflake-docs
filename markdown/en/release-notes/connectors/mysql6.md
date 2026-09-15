# Snowflake Connector for MySQL release notes

This topic provides release notes for the Snowflake Connector for MySQL.
For additional information, see [Snowflake connector for MySQL](https://other-docs.snowflake.com/en/connectors/mysql6/about).

## Version 6.11.2 (March 20, 2025)

### Behavior changes

- Reduced the number of INFO level logs in the agent for readability.
- The `_CONNECTORS_METADATA` and `JOURNALS` schemas were removed from the destination database in Snowflake. The connector can now only
  create journal tables in the database of the connector’s Snowflake Native App.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 6.10.1 (January 8, 2025)

### Behavior changes

- The snapshot load now resumes from the point of interruption. It’s supported only for specific column types described in [Resuming snapshot load after failures](https://other-docs.snowflake.com/en/connectors/mysql6/view-data#resuming-snapshot-load-after-failures).
  For other types, it starts from the beginning.
- The connector was optimized to result in a significant cloud services cost reduction.

### New features

Not applicable.

### Bug fixes

- Fixed a certain JDBC connection not being returned to the pool after use.
- The connector no longer creates short-lived tables, which increased cloud services usage.
- Fixed a bug when the database agent might enter an infinite loop when it couldn’t start incremental load for any table from a single data source.
- Snapshot and incremental replications do not fail on MySQL `DATE` or `DATETIME` values `0000-00-00` or values containing all zeroes in month or day. They are all replicated as `NULL`.

## Version 6.9.1 (December 12th, 2024)

### Behavior changes

- The native application has been migrated to the new [event-sharing model](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging). Telemetry sharing is now mandatory for all event types, such as logs and traces, and it can’t be disabled for the new installations. For already existing installations, you will receive an email with our account locator “EOA66985” asking you to review and configure the required event sharing.

### New features

Not applicable.

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
- Fixed replication errors when the *DEFAULT\_DDL\_COLLATION* parameter for account is set.

## Version 6.6.1 (October 3rd, 2024)

### Behavior changes

- The maximum connection pool size to source databases has been increased to 7.

### New features

Not applicable.

### Bug fixes

- The agent no longer stops after encountering data source connectivity issues.

## Version 6.6.0 (September 17th, 2024)

### Behavior changes

Not applicable.

### New features

- You can now configure the agent through environment properties in addition to using `snowflake.json` and `datasources.json` for configuration.
- You can now pass the private key contents through the `snowflake.private-key` property or `SNOWFLAKE_PRIVATEKEY` environment variable.

For more information, see [Configure and run the agent](https://other-docs.snowflake.com/en/connectors/mysql6/install-agent#configure-and-run-the-agent).

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
- Fixed agent failure when MySQL server enforces secure connection

## Version 6.4.0 (August 15th, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

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
