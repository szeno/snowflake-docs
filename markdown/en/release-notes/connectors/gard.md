# Snowflake Connector for Google Analytics Raw Data release notes

This topic provides release notes for the Snowflake Connector for Google Analytics Raw Data.

For additional information, see [Snowflake Connector for Google Analytics Raw Data](/connectors/google/gard/gard-connector-about).

## Version 2.13.0 (June 29, 2026)

### Behavior changes

Not applicable.

### New features

- Added the `CONFIGURE_CUSTOM_INGESTION_SCHEDULE` procedure, which lets you schedule data ingestion using a
  custom cron expression. For more information, see [Setting a custom ingestion schedule](/connectors/google/gard/gard-connector-managing#label-configure-custom-ingestion-schedule).

### Bug fixes

Not applicable.

## Version 2.12.0 (April 22, 2026)

### Behavior changes

- Manual reload now starts ingestion immediately instead of waiting for the next scheduled run.

### New features

Added a new option called `DISABLE_PRESENT_LOAD` to the `ENABLE_PROPERTIES` procedure:

- Default value is `FALSE`.
- Disables scheduled ingestion of data. When set to `TRUE`, the connector doesn’t trigger any automatic ingestion
  (except the initial load, if it’s enabled). You must reload data manually.
- Manual reloads can still trigger automatic reloads unless they are explicitly disabled.

### Bug fixes

- A failure to grant `SELECT` to the `DATA_READER` application role no longer stops ingestion from finishing.
- Added a check to ensure the `FRESH_DAILY` ingestion is still enabled before scheduling an automatic reload.
- Removed unused and misleading resource-related SDK procedures from the `PUBLIC` connector schema
  (`CREATE_RESOURCE`, `ENABLE_RESOURCE`, `DISABLE_RESOURCE`, `UPDATE_RESOURCE`, their `_VALIDATE`
  variants, and their `PRE_` / `POST_` hooks).

## Version 2.11.3 (April 15, 2026)

### Bug fixes

- The connector now grants `SELECT` privileges to the `DATA_READER` application role after every completed ingestion.
  This ensures privileges are correctly re-granted in case the user has removed them.

## Version 2.11.2 (August 19, 2025)

### Behavior changes

Not applicable.

### New features

Improved the logging for the connector operations. This improved logging includes the following more detailed information about BigQuery
streaming downloads:

- Download progress percentage
- Throttling information
- Amount of data downloaded in each batch

These improvements should help with troubleshooting streaming downloads that failed or ingestions that are stuck.

### Bug fixes

Not applicable.

## Version 2.11.1 (March 17, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

Fixed an issue where the connector was unable to ingest data from Google Analytics with the `QUOTED_IDENTIFIERS_IGNORE_CASE` account
parameter set to `true`.

## Version 2.11.0 (February 13, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

Restored support for the `USERS` and `PSEUDONYMOUS_USERS` export types.

## Version 2.10.0 (January 23, 2025)

### Behavior changes

Not applicable.

### New features

Added support for ingesting data by using the `FRESH_DAILY` export type:

- By default, the `FRESH_DAILY` export type is disabled. To enable it, call the `ENABLE_PROPERTIES` stored procedure. For details,
  see [Enabling or disabling the ingestion of a property](/connectors/google/gard/gard-connector-setting-up-data#label-gard-connector-enabling-ingestion).
- You can’t disable auto reloading data for the `FRESH_DAILY` export type. For more information,
  see [Updating data ingestion options](/connectors/google/gard/gard-connector-managing#label-update-data-ingestion-options).

### Bug fixes

Not applicable.

## Version 2.9.1 (January 15, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- The `USERS` and `PSEUDONYMOUS_USERS` export types, which in some cases caused the connector to stop responding when they were defined,
  are no longer defined in these cases.

## Version 2.9.0 (January 7, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue in the sink view where some columns were displayed multiple times.
- To reduce ingestion errors, Google OAuth2 security credentials are now refreshed more frequently.
- To optimize the performance of ingestion, Snowflake now limits the number of worker tasks that can use BigQuery data exports.

## Version 2.8.0 (December 3, 2024)

### Behavior changes

Not applicable.

### New features

- Migrated to telemetry v2.

### Bug fixes

- Data stream ingestions, which failed due to the `Out of Memory` errors, are now retried sooner.

## Version 2.7.1 (November 19, 2024)

### Behavior changes

Not applicable.

### New features

- Improved ingestion scalability.

### Bug fixes

Not applicable.

## Version 2.7.0 (October 31, 2024)

### Behavior changes

Not applicable.

### New features

- Added support for combinations of `DAILY`, `INTRADAY`, `USERS`, and `PSEUDONYMOUS_USERS` export types.
- Added support for multi-cluster warehouses.
- Performance and stability improvements.

### Bug fixes

Not applicable.

## Version 2.5.0 (October 24, 2024)

### Behavior changes

Not applicable.

### New features

- Historical data ingestion for new properties ingests in reverse chronological order, starting from the date on which the Google Analytics property was enabled, while the current data is ingested in parallel.

### Bug fixes

Not applicable.

## Version 2.4.0 (October 21, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 2.3.0 (October 7, 2024)

### Behavior changes

Not applicable.

### New features

Reloads of user data tables are now scheduled automatically after 72 hours.

### Bug fixes

- To prevent failures for a large number of properties, we’ve increased the timeout period
  on the view refresher task from 1 hour to 23 hours.
- Fixed issues related to identifier migration.
- Fixed the state of properties that got suspended due to an issue related to a race condition between
  refreshing the sink table views and disabling inaccessible Google Analytics properties.

## Version 2.2.1 (September 30, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Updated to Snowpark version 1.13.2 to address `ERROR_ON_NONDETERMINISTIC_UPDATE` error.

## Version 2.2.0 (September 27th, 2024)

### Behavior changes

Not applicable.

### New features

- Connectors now support the ingestion of the `USERS` and `PSEUDONYMOUS_USERS` export types.

### Bug fixes

- Fixed a race condition between the property cleaner and the view refresher.

## Version 2.1.0 (September 17th, 2024)

### Behavior changes

Not applicable.

### New features

- Added the `RESET_CONFIGURATION` procedure.

### Bug fixes

- Corrected missing parameters on dispatcher subprocess tasks.

## Version 2.0.0 (September 3rd, 2024)

### Behavior changes

Not applicable.

### New features

- Added support for identifiers in a worksheet format.

### Bug fixes

Not applicable.

## Version 1.8.2 (August 30th, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fix for issue causing PAUSE and RESUME procedures to fail.

## Version 1.8.0 (August 27th, 2024)

Internal updates only.

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 1.7.2 (August 19th, 2024)

### Behavior changes

Not applicable.

### New features

- Added flattened `event_params` and `user_properties` columns in the sink table views.
- Enabled change tracking on sink tables.
- Sink table views are now refreshed with the copy grants statement.

### Bug fixes

- Application upgrade fix for certain customers.

## Version 1.6.6 (August 12th, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Application upgrade fix for certain customers

## Version 1.6.3 (August 5th, 2024)

### Behavior changes

Not applicable.

### New features

- Sink table views are now refreshed automatically.
- Data is now synced sooner for timezones ahead of UTC.
- Improved scalability of scheduling ingestions for large number of properties.

### Bug fixes

Not applicable.

## Version 1.5.2 (July 18th, 2024)

### Behavior changes

Not applicable.

### New features

- New REFRESH\_VIEWS procedure, which allows recreating flattened data view.

### Bug fixes

Not applicable.

## Version 1.4.1 (July 8th, 2024)

### Behavior changes

Not applicable.

### New features

- Reloads are now scheduled automatically for all properties.
- Added [UPDATE\_INGESTION\_OPTIONS](/connectors/google/gard/gard-connector-managing#label-update-data-ingestion-options) procedure
  which allows customizing the ingestion settings for certain properties supporting two parameters:
  - EXCLUDE\_NULLS - do not ingest fields containing nulls values, which can increase performance.
  - DISABLE\_AUTO\_RELOADS - disable the auto reload mechanism for certain properties.

### Bug fixes

Not applicable.

## Version 1.3.0 (June 20th, 2024)

### Behavior changes

Not applicable.

### New features

- This release introduces the “reload property” feature. There are three new procedures for triggering reload:

  - `RELOAD_PROPERTY('<property id>')`
  - `RELOAD_PROPERTY('<property id>', <first date>, <last date>)`
  - `RELOAD_PROPERTY('<property id>', '<export type>', <first date>, <last date>)`
- There is one new procedure for canceling ongoing reload:

  - `CANCEL_RELOAD_PROPERTY('<load id>')`
- And a new view for observing ongoing reload:

  - `PUBLIC.ONGOING_RELOADS`

### Bug fixes

Not applicable.

## Version 1.2.0 (May 28th, 2024)

### Behavior changes

- Ingestion tasks are scaled based on warehouse size. Ingestion time for
  larger warehouses should be decreased.
- Additional optimizations in ingestion and ingestion scheduling.
  These updates could result in slightly lower credit consumption, as well as increased ingestion throughput.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 1.1.0 (May 22nd, 2024)

### Behavior changes

- Disabling property which is ingesting incremental intraday data will remove
  currently ingested day if ingestion was not fully completed.
- Introduced managed task to check and report its health back to Snowflake for
  Connectors installed before version 1.0.0. See the [Snowflake Connector for Google Analytics Raw Data health check cost](/connectors/google/gard/gard-connector-pricing#label-gard-connector-healthcheck-task-cost) for details.

### New features

Not applicable.

### Bug fixes

- Fixed issue with Pausing/Resuming Connector which left Connector state in intermediate state `PAUSING/ STARTING`.

## Version 1.0.1 (May 14th, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Dispatcher task was adjusted to never automatically suspend. See [SUSPEND\_TASK\_AFTER\_NUM\_FAILURES](/sql-reference/parameters#label-suspend-task-after-num-failures) for details.
- Ingestion worker tasks have prolonged timeout to 6h hours. This will override account level parameter settings.

## Version 1.0.0 (May 7th, 2024)

### Behavior changes

- Logging level is now set to INFO which should significantly decrease the
  amount of entries into the event table.
- The connector now runs a small, managed task to check and report its health
  back to Snowflake. See the [Snowflake Connector for Google Analytics Raw Data health check cost](/connectors/google/gard/gard-connector-pricing#label-gard-connector-healthcheck-task-cost)
  for details.

### New features

- New procedure `PUBLIC.UPDATE_CONNECTION` allows re-authenticating a running
  connector by providing a new set of external access and secret objects. See
  [Re-authentication of the connector](/connectors/google/gard/gard-connector-managing#label-re-authentication-of-the-connector)
  for details.
- Re-installing the connector, and configuring it over an existing set of destination tables, will
  now automatically re-enable their related Google Analytics properties for
  ingestion. This should make reinstalling the connector much faster.

### Bug fixes

- Tasks created by the connector now have a fixed set of properties, mostly
  related to `AUTOCOMMIT` and date-time formats, required for these tasks to
  work correctly. These will override account-level properties.

  Operating on the
  connector by explicitly calling its functions or procedures still requires
  certain default values, as described in
  [Snowflake Connector for Google Analytics Raw Data known limitations](/connectors/google/gard/gard-connector-about#label-gard-connector-about-limitations).

## Version 0.19.2 (May 6th, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue with refreshing OAuth access tokens that was causing long-running ingestions to fail.

## Version 0.19.0 (April 26th, 2024)

### Behavior changes

Not applicable.

### New features

- A new procedure `PUBLIC.UPDATE_WAREHOUSE` is now available to
  replace the warehouse used by the connector.
- Scheduling ingestions should now be much faster, especially for instances
  configured with large numbers of Google Analytics properties.

### Bug fixes

Not applicable.

## Version 0.18.0 (April 15th, 2024)

### Behavior changes

Not applicable.

### New features

- The procedure `UPDATE_CONNECTION_CONFIGURATION` was introduced. It can be
  used for re-authentication purposes. Connector has to be paused to use this
  procedure. Currently it is only available from the worksheet and takes one argument
  type of VARIANT composed of fields: `external_access_integration`,
  `security_integration` and `secret`.

### Bug fixes

Not applicable.

## Version 0.16.4 (April 11th, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue with disrupted scheduling of ingestions during execution of dispatcher task.

## Version 0.16.3 (April 8th, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue where changing the ingestion schedule while the
  dispatcher task was running could lead to temporary duplication of the dispatcher task.

## Version 0.16.2 (March 25th, 2024)

### Behavior changes

- The connector now requests permission to `EXECUTE MANAGED TASK`. This
  is in preparation for internal monitoring features that will help us
  discover and address issues earlier.

### New features

Not applicable.

### Bug fixes

- Fixed an issue where changing the ingestion schedule while the
  dispatcher task was running could corrupt the internal state of the
  connector so that it would not be able to schedule further ingestions.

## Version 0.16.1 (March 19th, 2024)

Versions released in between this and prior release notes had only internal
changes, and thus no release notes were published.

### Behavior changes

Not applicable.

### New features

- A number of optimizations made to scheduling ingestions and ingesting itself.
  This should result in slightly lower credit consumption, as well as increased
  ingestion throughput, especially on tables with fewer than one million records.
- The connector now supports mixed-case and lowercase secret names.

### Bug fixes

- Ingestions should no longer fail due to issues with refreshing the access
  token. This may very rarely still occur for particularly large tables, but
  will always be re-tried by the connector automatically.
- Added validation to prevent enabling the same Google Analytics property
  ingestion from multiple Google Cloud Platform projects.
- Enabling multiple properties at once is now more resilient against issues with
  BigQuery connectivity. It will only fail the properties for which it
  couldn’t connect to BigQuery, and successfully enable all the others.

## Version 0.11.1 (February 12th, 2024)

### Behavior changes

- Several stored procedures, meant specifically for early user interface, access were removed.
  These stored procedures were generally not documented,
  and not part of our public API, but they may have been visible when listing
  procedures exposed by the connector. There’s no change in how the connector
  works, or how it should be operated.
- The procedure `CONFIGURE_CONNECTION` now requires an additional parameter `security_integration`
  with the name of the security integration created for
  the connector. This applies only for worksheet-based setups. If you’re setting
  the connector up via the user interface, this change is transparent to you.

### New features

- Updated links to the connector’s documentation.

### Bug fixes

- Improved reading tables available in BigQuery to ensure we only look at
  Google Analytics export tables, and filter out similarly-named tables. This
  issue could sometimes cause enabling new properties, or ingesting enabled
  properties to fail.

## Version 0.10.1 (January 26th, 2024)

Initial public preview release.

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

Not Applicable
