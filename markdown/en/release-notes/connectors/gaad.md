# Snowflake Connector for Google Analytics Aggregate Data release notes

This topic provides release notes for the Snowflake Connector for Google Analytics Aggregate Data. For additional
information, see [Snowflake Connector for Google Analytics Aggregate Data](/connectors/google/gaad/gaad-connector-about).

## Version 2.2.2 (December 3rd, 2025)

### Bug fixes

- Fixed an issue where the report start date was calculated incorrectly when report ingestion exceeded 2 hours.

## Version 2.2.1 (November 7th, 2024)

### Behavior changes

- Event sharing is now mandatory for all event types.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 2.2.0 (October 29th, 2024)

### Behavior changes

- Revoked the USAGE privilege on the `STATE` schema from the ADMIN application role.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 2.1.2 (October 16th, 2024)

### Bug fixes

- The `IMPORT_STATE` procedure now grants `SELECT` privilege to the application roles `ADMIN` and `DATA_READER`.

## Version 2.1.1 (October 16th, 2024)

### Bug fixes

- Export process failed. Scoped temporary tables could not be created in the destination schema.

## Version 2.1.0 (October 16th, 2024)

### Behavior changes

- The connector creates additional tables in destination schema. The tables are used to store the configuration of the connector. The tables have \_SFSDKEXPORT\_V1 suffix.

### New features

- IMPORT\_STATE procedure was added. The procedure can be used to recover a configuration of the reports, schedules, and history of the ingestions after the connector was uninstalled.

### Bug fixes

Not applicable.

## Version 2.0.0 (September 16th, 2024)

### Behavior changes

- The connector requires all configured identifiers to be quoted based on the
  [identifier requirements](/sql-reference/identifiers-syntax).

### New features

- Report tables have `change_tracking` enabled.
- You can now reset the connector’s configuration before the configuration is finalized using the `RESET_CONFIGURATION` procedure.
- You can now recover a connector in the `ERROR`, `PAUSING`, or `STARTING` state using the `RECOVER_CONNECTOR_STATE` procedure.

### Bug fixes

Not applicable.

## Version 1.5.0 (July 22nd, 2024)

### Behavior changes

Not applicable.

### New features

- Reports can now be configured to avoid sampling by shortening ingestion interval length.

### Bug fixes

- Corrected handling of quoted identifiers in the GET\_TROUBLESHOOTING\_DATA procedure.
  See also [Troubleshooting](/connectors/google/gaad/gaad-connector-troubleshooting).

## Version 1.4.0 (June 28th, 2024)

### Behavior changes

- Sampling metadata is available in the CONNECTOR\_STATS view.
- The connector saves INGESTION\_RUN\_ID in tables with report data.

### New features

Not applicable.

### Bug fixes

- To avoid ingestion timeouts, existing task timeouts have been increased to 4 hours.
- Worker tasks can be rescheduled to avoid timeouts during ingestion.

## Version 1.3.1 (June 26th, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Timeout for new tasks has been increased to 4 hours to prevent timeouts during ingestion.

## Version 1.3.0 (June 19th, 2024)

### Behavior changes

The minimal interval used during ingestion runs has been reduced to one day.

### New features

- Added the `UPDATE_WAREHOUSE` procedure.

### Bug fixes

The `CONFIGURE_REPORT` procedure can now be called in parallel.

## Version 1.2.0 (May 24th, 2024)

### Behavior changes

Not applicable.

### New features

- Added the healthcheck task to all connector instances.

### Bug fixes

Not applicable.

## Version 1.1.1 (May 21st, 2024)

### Behavior changes

Not applicable.

### New features

- Added the `UPDATE_CONNECTION_CONFIGURATION` procedure.

### Bug fixes

Not applicable.

## Version 1.0.1 (May 13th, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed issue where the connector could enter an inconsistent state during pausing or resuming.

## Version 1.0.0 (April 29th, 2024)

### Behavior changes

- The CONFIGURE\_REPORT procedure returns validation errors instead of throwing them.
- The connector will wait for 30 seconds before retrying ingestion after a 502 error.
- Worker tasks will not be suspended due to errors.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 0.25.0 (April 24th, 2024)

### Behavior changes

- The connector tries to avoid 502 errors by reducing the date range for large reports.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 0.24.0 (April 9th, 2024)

### Behavior changes

- The `CONNECTOR_EXECUTION_LOG` table is no longer visible to users.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 0.23.1 (April 4th, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed start date calculation (in some cases, the start date could be set
  after the end date due to timezone differences).

## Version 0.23.0 (April 3rd, 2024)

### Behavior changes

- Date ranges for initial and incremental loads are split into 31-day intervals to
  reduce the number of 502 API errors.

### New features

Not applicable.

### Bug fixes

- Added metadata column to the `PUBLIC.CONNECTOR_STATS` view and to the
  result of `GET_TROUBLESHOOTING_DATA` procedure.

## Version 0.22.0 (March 26th, 2024)

### Behavior changes

Not applicable.

### New features

- Added the `GET_TROUBLESHOOTING_DATA` procedure

### Bug fixes

Not applicable.

## Version 0.21.1 (March 20th, 2024)

### Behavior changes

- Added request for the `EXECUTE MANAGED TASK` privilege to the connector’s manifest.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 0.21.0 (March 19th, 2024)

### Behavior changes

- The `CONNECTOR_EXECUTION_LOG` table is deprecated and will be removed in the future.

### New features

- Added more details to the `CONNECTOR_ERRORS` view, including the error reason.

### Bug fixes

- The `CONNECTOR_CONFIGURATION`, `CONNECTOR_STATS`, and `CONNECTOR_ERRORS` views are now visible to the `VIEWER` application role.

## Version 0.20.0 (March 14th, 2024)

### Behavior changes

- Internal changes only.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 0.19.0 (March 12th, 2024)

### Behavior changes

Not applicable.

### New features

- Added alerting handling. Procedures `DISABLE_ALERTS` and `CONFIGURE_ALERTS` were added.

### Bug fixes

Not applicable.

## Version 0.18.0 (March 7th, 2024)

### Behavior changes

Not applicable.

### New features

- Generated IDs for all CONNECTOR\_EXECUTION\_LOG entries.

### Bug fixes

- Fixed initial load start date calculation.

## Version 0.17.0 (February 22nd, 2024)

### Behavior changes

- The retry count for GA API requests was reduced to 1, and removed retries for 502 errors.

### New features

- Added ID column to CONNECTOR\_EXECUTION\_LOG. The column will be populated for new entries.

### Bug fixes

Not applicable.

## Version 0.16.0 (February 16th, 2024)

### Behavior changes

Not applicable.

### New features

- Added views containing basic ingestion statistics - `CONNECTOR_STATS` and `AGGREGATED_CONNECTOR_STATS`.
- Added a view containing ingestion errors - `CONNECTOR_ERRORS`.
- Added a procedure that immediately triggers ingestion for a given report - `INGEST_NOW(<report name>)`.
- Added a function to retrieve dimensions and metrics for a given property - `GET_DIMENSIONS_AND_METRICS(<property id>)`.

### Bug fixes

Not applicable.

## Version 0.15.0 (February 1st, 2024)

### Behavior changes

- Date ranges for initial ingestion are split into 6-month intervals. This reduces the risk of initial load failing for reports with a distant start date.
- Updated links to the documentation in prerequisites and README file.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 0.14.0 (January 29th, 2024)

### Behavior changes

Initial version.

### New features

Not applicable.

### Bug fixes

Not applicable.
