# Snowflake Connector for ServiceNow® V2 release notes

This topic provides release notes for the Snowflake Connector for ServiceNow® V2. For additional
information, see
[Snowflake Connector for ServiceNow](https://other-docs.snowflake.com/en/connectors/servicenow/v2/about).

## Version 5.28.1 (August 19, 2026)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue where ingestion or a table reload could retry indefinitely with the same page size after the ingestion
  procedure ran out of memory. The connector now reduces the page size before retrying.
- Fixed a data-loss issue in tables that have row filtering enabled. When ServiceNow® returned no rows in response to a
  query for records with an empty `sys_updated_on` or `sys_created_on` value, the connector could delete every row in
  the table.
- Fixed an issue where the incremental update window didn’t advance when a run fetched no rows. The window collapsed
  to zero width, which prevented any further records from being ingested for the affected table.
- Fixed the same issue in the deletions synchronization window. This issue caused every subsequent run to rescan the
  journal table from an outdated timestamp.
- Fixed an issue where the connector didn’t warn when it skipped records whose `sys_updated_on` or `sys_created_on`
  values it couldn’t read. For example, a ServiceNow® field-level access control list can hide either column from the
  connector user. If an access control list caused records to be skipped, correct the list and then reload the affected
  tables with the `RELOAD_TABLE` procedure. For more information, see
  [Reload data in a table](/connectors/servicenow/ingestion#label-servicenow-connector-reload-table).

## Version 5.28.0 (June 29, 2026)

### Behavior changes

Not applicable.

### New features

- Added the `CONFIGURE_SCAN_EVENT_LOG_IN_INCREMENTAL` stored procedure. When set to `false`, incremental
  ingestion no longer probes the `__EVENT_LOG` table to classify each fetched row as an `INSERT` or `UPDATE`.
  On accounts with large `__EVENT_LOG` tables, doing so avoids scanning a large amount of data during every batch.
  The default is `true`, which preserves the existing behavior. For more information, see [Configure the event log scan during incremental ingestion](/connectors/servicenow/ingestion#label-servicenow-connector-configure-scan-event-log-incremental).
- Added the `CONFIGURE_CHECK_LINK_IN_VIEW_WITH_REFERENCES` stored procedure. When set to `false`, views created
  using the `CREATE_VIEW_WITH_DISPLAY_VALUES` stored procedure do not check the `link` property of the raw ServiceNow®
  row, which lets you use non-standard reference links. The default is `true`, which preserves the existing
  behavior. For more information, see [Configure reference link checking for views](/connectors/servicenow/accessing-data#label-servicenow-connector-configure-check-link-in-view-with-references).
- Added support for checking empty values in row filtering, for example, `u_name = ""`. For more information, see [Enable a single table by using row filtering](/connectors/servicenow/ingestion#label-servicenow-connector-row-filtering).

### Bug fixes

Not applicable.

## Version 5.27.4 (March 5, 2026)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue that caused alert emails to be sent too often and with incorrect error data.

## Version 5.27.3 (February 17, 2026)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed a possible race condition during the reload finalization process.

## Version 5.27.2 (January 21, 2026)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue where display values were not processed correctly when ingesting rotated tables.
- Improved logging in the alerting system.

## Version 5.27.1 (Nov 25, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Changed the column used for API request length validation.

## Version 5.27.0 (Oct 29, 2025)

### Behavior changes

- The connector no longer has a `128 MB` memory limit for uncompressed responses from the ServiceNow API.

### New features

Not applicable.

### Bug fixes

Not applicable.

## Version 5.26.0 (Oct 1, 2025)

### Behavior changes

- Custom journal tables are currently disabled. They’ll be restored with new functionality in a future release.
- When you pause the connector, only worker tasks are forcefully canceled. Other tasks keep running until they finish, so pausing might take a bit longer.

### New features

- The connector now lets you use `NOT LIKE` and `NOT IN` operators for row filtering, so you can filter your data more flexibly during ingestion.

### Bug fixes

- The connector now retries `curl` errors more times, making it more resilient to network issues in Azure deployments.

## Version 5.25.2 (Sep 12, 2025)

### Behavior changes

Not applicable.

### New features

- Improved logging of HTML responses.
- Improved error handling for External Access.

### Bug fixes

Not applicable.

## Version 5.25.1 (Sep 10, 2025)

### Behavior changes

Not applicable.

### New features

- Improved handling of large response sizes during data decompression by reducing the page size when necessary.

### Bug fixes

Not applicable.

## Version 5.25.0 (Sep 5, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue that caused the schema table to be created incorrectly during state import.
- Fixed an issue in filtered reload mode where some state events could be saved in the wrong order, which could lead to missed updates.
- Improved handling of large responses from ServiceNow.
- Added more detailed logging for ServiceNow response properties.

## Version 5.24.0 (Jun 23, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue that could cause the metadata tables to be ingested incorrectly during reload when the connector is globally configured to fetch display values.
  As a result of this issue, flattened views were not created for some tables. If this issue
  occurred, the following metadata tables had to be reloaded:
  - `sys_dictionary`
  - `sys_db_object`
  - `sys_glide_object`

## Version 5.23.0 (Jun 12, 2025)

### Behavior changes

- For records in the `sys_created_on` or `sys_updated_on` columns with null values, the connector inserts an update event only when the
  record has changed since the last ingestion. Previously, the connector inserted an update event to the event log table during each
  ingestion cycle, regardless of whether the record changed. This behavior could cause the event log table to grow indefinitely, even
  if no changes were found in the table.

### New features

Not applicable.

### Bug fixes

- Increased the range of page sizes that the connector tries during filtered ingestion. When fetching data, the connector should now be
  more resilient to timeout errors that come from the ServiceNow® API.
- Fixed the internal cleanup job to retain internal connector information that is needed to perform ingestion. Previously, when this
  information was removed, it could cause ingestion failures.
- Fixed an error during the creation of flattened views. This error was caused by a missing column in the internal connector table.

## Version 5.22.3 (May 26, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue with page size persistence when reloading a table.

## Version 5.22.1 (Apr 28, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue that could cause the export of the connector state to fail when row filtering expressions are used on string values.

## Version 5.22.0 (Apr 24, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue that could cause an HTTP response parsing failure. In some cases, this issue could cause the connector to fail to ingest
  data from ServiceNow®.

## Version 5.21.0 (Apr 15, 2025)

### Behavior changes

Not applicable.

### New features

- Added support for continuous schedules. You can use this feature to set an ingestion schedule for up to 20 tables that will be executed
  every one minute. Snowflake recommends using continuous schedules carefully and only for tables that require near-real-time data in
  Snowflake. To enable this feature, you can use the `ENABLE_TABLE` or `CONFIGURE_TABLES_SCHEDULE` procedures. To learn more, see
  [Specifying the Synchronization Schedule](https://other-docs.snowflake.com/en/connectors/servicenow/ingestion#specifying-the-synchronization-schedule).
- The maximum number of tables that can be ingested concurrently has been increased from 30 to 50. This update allows for better warehouse
  utilization and improves overall performance. To learn more, see [Scaling the connector](https://other-docs.snowflake.com/en/connectors/servicenow/managing#scaling-the-connector).

### Bug fixes

- The connector is more stable and more performant when ingesting multiple tables in parallel.

## Version 5.20.0 (Apr 8, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed a bug that caused the export of the connector state to fail.

## Version 5.19.1 (Mar 25, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed a bug that caused the parsing process of the API response from ServiceNow® to fail when a header name in the response didn’t match the expected format.
- Fixed a bug that caused the export of the connector state and configuration to fail, when a filtered reload was run on a table.

## Version 5.19.0 (Mar 20, 2025)

### Behavior changes

Not applicable.

### New features

- The `DELETE_TABLE` procedure now accepts an optional `drop_related_objects` boolean parameter.
  When this parameter is set to `true`, the procedure drops all the objects related to the table,
  such as the flattened views, the event log table, and the sink table.
- The filtered reload feature now supports detection of deletes and can filter out these records
  when using the `sys_ids` parameter in the `RELOAD_TABLE` procedure.
  Prior to this release, the filtered reload feature only detected data updates and insertion.

### Bug fixes

- Corrected error in `CONNECTOR_STATS` view ingested row statistics when running filtered reload.

## Version 5.18.1 (Mar 10, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Reverted a performance optimization that could cause increased warehouse consumption.

## Version 5.18.0 (Feb 28, 2025)

### Behavior changes

- To see the configuration details for tables you reload, use the new `RELOADED_TABLES` view instead of the `CONFIGURED_TABLES` view.
  This new view includes the configuration values for the table from the `CONFIGURED_TABLES` view plus new columns that
  provide information about the reload configuration that was used for the table and the reload status for the table. For more information,
  see [About Monitoring the Connector](https://other-docs.snowflake.com/connectors/servicenow/monitoring#about-monitoring-the-connector).

### New features

- Added support for OAuth client credentials grant flow. When setting up OAuth, we recommend that you use this flow instead of OAuth
  authentication code grant flow. For more information, see
  [Setting up OAuth](https://other-docs.snowflake.com/en/connectors/servicenow/installing-sql#setting-up-oauth). If the connector is
  already configured with another OAuth flow and then you configure it to use the client credentials grant flow, we recommend that you perform the following tasks, if possible:

  - Recreate the secret and security integration objects to use client credentials. For instructions, see
    [Creating a security integration and Creating a secret object](https://other-docs.snowflake.com/en/connectors/servicenow/installing-sql#creating-a-security-integration-optional).
  - Update the connection to ServiceNow instance to use new credentials. For more information, see
    [Updating the connection to ServiceNow® instance](https://other-docs.snowflake.com/en/connectors/servicenow/managing#updating-the-connection-to-servicenow-instance).
- Added a new config parameter to the `RELOAD_TABLE` procedure. This parameter allows you to reload specific records in a table instead of the
  whole table. For details, see [Filtered reload](https://other-docs.snowflake.com/en/connectors/servicenow/ingestion#filtered-reload).
- In views containing reference fields, columns with the `__DISPLAY_VALUE` suffix that contain data for reference fields now display the
  most recent data. Previously, these columns always returned the display value for the ingested raw
  value from the same table. To enable this feature, including in existing views, call the `CREATE_VIEW_WITH_DISPLAY_VALUES` stored procedure.
  For more information, see [Creating a View Containing Reference Fields](https://other-docs.snowflake.com/connectors/servicenow/accessing-data#creating-a-view-containing-reference-fields).

### Bug fixes

- Improved the performance of the initial test request when a new table is enabled for ingestion.
- Improved error handling when the returned error code is in a different format than expected.

## Version 5.17.1 (Feb 7, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

Fixed an issue where the reference columns in flattened views displayed incomplete data when the view contained data from a table with
`fetch_display_values` enabled.

## Version 5.17.0 (Jan 31, 2025)

### Behavior changes

The flattened views now always display columns in alphabetical order. Previously, these views sometimes displayed columns in random
order.

### New features

Not applicable.

### Bug fixes

- Fixed an issue where data included in a view would shift between columns when the view contained reference fields.
- Fixed an issue where flattened views weren’t recreated correctly.
- For tables with `fetch_display_values` enabled, fixed an issue where the connector only retrieved a single page of up to 10,000 records
  for a table before the ingestion process stopped. However, you must reload these tables to apply the fix to them, including tables
  with `fetch_display_values` enabled through the global connector settings. For instructions on how to reload a table, see
  [Reloading Data in a Table](https://other-docs.snowflake.com/connectors/servicenow/ingestion#reloading-data-in-a-table).

## Version 5.16.1 (Jan 24, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

Fixed an issue where calling the `CONFIGURE_DISPLAY_VALUE_FETCHING` stored procedure would fail to configure the default display values for
tables and cause the Snowflake Connector for ServiceNow® V2 to stop responding.

## Version 5.16.0 (Jan 15, 2025)

### Behavior changes

Not applicable.

### New features

- A new `CONFIGURE_DISPLAY_VALUE_FETCHING` procedure was added. It is used to set global, default configuration for handling display values.
  Display value synchronization can also be configured on the table level, using the `ENABLE_TABLE` procedure.
- Data with resolved display values can now be fetched, instead of only raw data.

### Bug fixes

- Fixes for the connector state export process.
- Improved handling of DNS errors.
- `CREATE_VIEW_WITH_DISPLAY_VALUES` and `ENABLE_REFERENCED_TABLES` procedures now handle included columns configuration.

## Version 5.15.2 (Jan 7, 2025)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- The connector now handles an exception when a table that is getting exported has incomplete configuration.
- The upgrade process no longer fails if the `GET_TROUBLESHOOTING_DATA` procedure doesn’t get created.
- The connector no longer fails when an internal state snapshot isn’t created because of its size.

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
