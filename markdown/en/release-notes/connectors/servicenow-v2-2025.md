# Snowflake Connector for ServiceNow® V2 release notes for 2025

This topic provides release notes for the Snowflake Connector for ServiceNow® V2. For additional
information, see
[Snowflake Connector for ServiceNow](https://other-docs.snowflake.com/en/connectors/servicenow/v2/about).

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
