# Snowflake Connector for ServiceNow® V2 release notes for 2024

This topic provides release notes for the Snowflake Connector for ServiceNow® V2. For additional
information, see
[Snowflake Connector for ServiceNow](https://other-docs.snowflake.com/en/connectors/servicenow/v2/about).

## Version 5.15.1 (Dec 6, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Added migration to support old sync states in data export.

## Version 5.15.0 (Dec 3, 2024)

### Behavior changes

- The export process to store the connector internal state changed.

  In addition to storing metadata in the `__CONNECTOR_STATE_EXPORT` table, the data is also split into multiple tables with a `_SFSDKEXPORT_V1` suffix.

### New features

- Snowflake Connector for ServiceNow® V2 now supports disaster recovery in another region.
- Added support for configuring deletion synchronization at the table level using the `ENABLE_TABLE` procedure.

  For more information on using the `ENABLE_TABLE` procedure, see
  [Enabling a single table using custom configuration](https://other-docs.snowflake.com/en/connectors/servicenow/v2/ingestion#label-servicenow-connector-configure-custom-configuration-v2).

### Bug fixes

- Unexpected responses from the ServiceNow API are now correctly handled in the procedures such as `CHECK_ROW_COUNT`.

## Version 5.14 (Nov 18, 2024)

### Behavior changes

- Event sharing is now mandatory for new installations.

### New features

- You can now set a specified table page size with the `RESET_PAGE_SIZE` procedure instead of using the default connector’s value.
- If the connector’s default page size was set to an invalid value, the connector will use the recommended value of 10,000.

### Bug fixes

- Ingestion fails when a worker task reaches API timeout when discovering the initial table page size.

## Version 5.13 (Oct 29, 2024)

### Behavior changes

Not applicable.

### New features

- Add timeout on establishing the http connection.

### Bug fixes

Not applicable.

## Version 5.12 (Oct 16, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Incremental updates no longer fail if Snowflake doesn’t receive the timestamp of the newest record on the ingested table.

## Version 5.11.1 (Oct 8, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Incremental updates no longer fail when the event log table is empty.
- Incremental ingestion no longer fails when a fetched batch is empty due to having out-of-date
  rows during record updates from the source.

## Version 5.11.0 (Oct 7, 2024)

### Behavior changes

Modified the ServiceNow API request sorting rules applied during incremental updates to eliminate data loss while reading data from multiple read replicas.

### New features

Not applicable.

### Bug fixes

Page size is no longer reduced when the ServiceNow instance is not reachable.

## Version 5.10.1 (Sep 6, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed configuration validation in the `UPDATE_CONNECTION_CONFIGURATION` procedure.

## Version 5.10.0 (Aug 30, 2024)

### Behavior changes

- A request for the most recent timestamp is added at the beginning of updates and deletes.

### New features

- The `UPDATE_CONNECTION_CONFIGURATION` procedure is added. This procedure lets you change External Access Integration and Secret objects used by the connector.
- User Agent header in connector HTTP requests is now set to `snowflake-connector-for-service-now`.

### Bug fixes

- Handle HTTP Client timeout errors gracefully.

  Reduce page size on such an error.
- ServiceNow® and Snowflake time differences no longer cause data to be lost.

## Version 5.9.1 (Aug 14, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Migration script fix for certain users.

## Version 5.9.0 (Aug 8, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fix `RELOAD_TABLE` procedure when both `row_filter` and `data_range_start_time` are set.
  Previously row filtering sync states were not cleaned up correctly.
- Improve error handling in the data ingestion process when the connector is not able to overcome
  errors related to authentication. In such cases, the connector should now be able to
  detect the error earlier and stop the ingestion process.

## Version 5.8.0 (Jul 23, 2024)

### Behavior changes

Not applicable.

### New features

- The `row_filter` field in `ENABLE_TABLE` procedure now accepts arbitrary number of whitespace characters
  in filtering expression rather than allowing only single space between expression elements.

  For more information see [Enabling a single table using custom configuration](https://other-docs.snowflake.com/en/connectors/servicenow/v2/ingestion#label-servicenow-connector-configure-custom-configuration-v2).

### Bug fixes

- During table reload row filter and column filtering now taken into account.
- Row filter now works as expected for tables without a `sys_updated_on` column

## Version 5.7.0 (Jul 11, 2024)

### Behavior changes

Not applicable.

### New features

Procedures CHECK\_ROW\_COUNT, ENABLE\_TABLE (without custom configuration parameters) and
SHOW\_REFERENCES\_OF\_TABLE can now be called in a user-owned task.

### Bug fixes

Not applicable.

## Version 5.6.0 (Jul 5, 2024)

### Behavior changes

Not applicable.

### New features

Row filtering is now available. Row filtering supports the filtering of ingested table rows based on
conditions evaluated against table columns.
The row filtering condition is set using the `ENABLE_TABLE` procedure.

For more information see Enabling a single table using custom configuration in
[Setting Up data ingestion for your ServiceNow® data](https://other-docs.snowflake.com/en/connectors/servicenow/v2/ingestion#label-servicenow-connector-configure-custom-configuration-v2).

### Bug fixes

Improve performance of the migration script from prior version.

## Version 5.5.1 (Jun 28, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

Improve performance of the migration script from prior version.

## Version 5.5.0 (Jun 24, 2024)

### Behavior changes

Not applicable.

### New features

Add a default way to obtain the schema of a table when starting its
ingestion. This should help in a scenario where the connector couldn’t start to
ingest a table because of ACLs met on the first ingested row.

### Bug fixes

- Fix `RUN_HEALTHCHECK` as it sometimes could fail to send the connector’s status in a specific scenario.

## Version 5.4.0 (Jun 10, 2024)

### Behavior changes

Not applicable.

### New features

Change endpoint for fetching schema of the table. From version 5.4.0 and later, the `ADMIN` role
in ServiceNow® is no longer required to use `CREATE_VIEW_WITH_DISPLAY_VALUES`,
`SHOW_REFERENCES_OF_TABLE` and `ENABLE_TABLE` (when using column filtering)
procedures.

### Bug fixes

From version 5.4.0 and later, new event log table `DELETE` events include the `RAW` column, which is set
to a value from the newest update event instead of the first insert event.
Previously existing event log table events remain unchanged.

## Version 5.3.0 (May 17, 2024)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

Fix handling the null value of the `journal_table` property in the object passed to
the `FINALIZE_CONNECTOR_CONFIGURATION` procedure. The `journal_table` parameter can now also be skipped.

## Version 5.2.0 (May 10, 2024)

### Behavior changes

Not applicable.

### New features

Add optional table\_name and `sys_id` arguments to `FINALIZE_CONNECTOR_CONFIGURATION` to
help in journal table validation.

### Bug fixes

- Improve URL validation in `SET_CONNECTION_CONFIGURATION` to support custom ServiceNow® domains.

## Version 5.1.0 (Apr 29, 2024)

### Behavior changes

Not applicable.

### New features

`max_sys_created_on` argument in `CHECK_ROW_COUNT` procedure now defaults to `NULL`.

### Bug fixes

- Don’t start healthcheck reporting if the configuration hasn’t successfully completed.
- Fix `SHOW_REFERENCES_OF_TABLE` to include self-references of a given table in returned value.
- Fix `CREATE_VIEW_WITH_DISPLAY_VALUES` to handle situation when table references itself.

## Version 5.0.0 (Apr 23, 2024)

Initial release with version 5.0.0.

### Behavior changes

- External function making API calls to ServiceNow® are replaced with external access.
- Signatures and behavior of many procedures changed. Division of responsibility can be checked in the below table:

> |  |  |
> | --- | --- |
> | Prior procedure | New procedure |
> | `CONFIGURE_CONNECTOR` | Several specialized procedures `CONFIGURE_*`. |
> | `CONFIGURE_WAREHOUSE` | `UPDATE_WAREHOUSE` |
> | `STOP_CONNECTOR` | `PAUSE_CONNECTOR` |
> | `START_CONNECTOR` | Several procedures to install the app when using worksheets. |
> | `PREFILL_CONFIG_TABLE` | `GET_AVAILABLE_TABLES` |
> | `ENABLE_TABLE_WITH_COLUMNS` | `ENABLE_TABLE` |
> | `ENABLE_TABLES(VARCHAR, BOOLEAN)` | `ENABLE_TABLES(ARRAY), DISABLE_TABLES(ARRAY)` |
> | `TEST_SN_CONNECTION` | `TEST_CONNECTION` |
> | `CHECK_SN_ROW_COUNT` | `CHECK_ROW_COUNT` |
> | `GET_STATUS` | - |
> | `GET_CONNECTION_STATUS` | - |
> | `GET_VERSION` | - |
> | `RUN_UPGRADE` | - |
>
> Expand
>
> Show lessSee more

- Procedures return an object with `response_code` property. The procedure
  result with an optional error reason is displayed directly in the response.
- Signatures and behavior of several views changed. Division of responsibility
  can be checked in the below table:

  |  |  |
  | --- | --- |
  | Prior view | New view |
  | `ENABLED_TABLES` | `CONFIGURED_TABLES`, `TABLES_STATE` |
  | `CONNECTOR_RUNS_STATE` | Included in `GET_TROUBLESHOOTING_DATA` procedure. |
  | `CONNECTOR_STATS` | `AGGREGATED_CONNECTOR_STATS` |
  | - | `SYNC_STATUS` |

  Expand

  Show lessSee more

### New features

Not applicable.

### Bug fixes

Not applicable.
