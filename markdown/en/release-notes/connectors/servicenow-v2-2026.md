# Snowflake Connector for ServiceNow® V2 release notes for 2026

This topic provides release notes for the Snowflake Connector for ServiceNow® V2. For additional
information, see
[Snowflake Connector for ServiceNow](https://other-docs.snowflake.com/en/connectors/servicenow/v2/about).

## Version 5.29.1 (October 28, 2026)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue where the `EXPORT_CONNECTOR_STATE` procedure and the scheduled state export failed with the error
  `Cannot parse sync state json value fetched from database to object`. This issue occurred after the deletions
  synchronization of a table processed journal entries on version 5.29.0. The connector now exports and imports the new
  fields of the deletions synchronization state. After you upgrade, call the `EXPORT_CONNECTOR_STATE` procedure again,
  or wait for the next scheduled export. For more information, see
  [Exporting the connector state](/connectors/servicenow/managing#label-servicenow-connector-exporting-connector-state-v2).

## Version 5.29.0 (October 23, 2026)

### Behavior changes

- Requests that return invalid JSON are now retried once after 30 seconds. If the retry also fails, the connector
  reduces the page size. Previously, the connector reduced the page size immediately. For more information, see
  [Configure the size of a single page fetch for a table](/connectors/servicenow/ingestion#label-servicenow-connector-configure-page-size).
- The `INGESTED_ROWS` value in the `CONNECTOR_STATS` view is now 0 for `DELETES` runs that find no new journal
  entries. Previously, it counted the duplicate `DELETE` events that those runs inserted again. This change doesn’t
  indicate lost progress.

### New features

- Added the `CONFIGURE_EXCLUDE_INACTIVE_COLUMNS_FROM_VIEWS` stored procedure. When set to `true`, columns that are
  inactive or deleted in the ServiceNow® `sys_dictionary` table are excluded from the `__view` and
  `__view_with_deleted` views the next time the connector creates the views. The setting doesn’t apply to tables with
  column filtering. You must recreate `__view_with_references` views with the `CREATE_VIEW_WITH_DISPLAY_VALUES` stored
  procedure for the change to apply to them. The default is `false`, which preserves the existing behavior. For more
  information, see [Exclude inactive columns from views](/connectors/servicenow/accessing-data#label-servicenow-connector-configure-exclude-inactive-columns-from-views).

### Bug fixes

- Fixed an issue where calling the `CONFIGURE_DISPLAY_VALUE_FETCHING`, `CONFIGURE_SCAN_EVENT_LOG_IN_INCREMENTAL`, or
  `CONFIGURE_CHECK_LINK_IN_VIEW_WITH_REFERENCES` stored procedure with `NULL` stored `false` instead of returning an
  `INVALID_CONFIGURATION` error.
- Fixed an issue where ingestion didn’t reduce the page size when the External Access function ran out of memory.
  Tables with large rows kept failing with the error `Function available memory exhausted`. For more information, see
  [Configure the size of a single page fetch for a table](/connectors/servicenow/ingestion#label-servicenow-connector-configure-page-size).
- Fixed an issue where the deletions synchronization inserted the `DELETE` events of the most recently processed journal
  entries again on every run, as long as no newer journal entry appeared. The connector still rescans the last second
  of the journal to catch late-arriving entries, but it now skips the entries it already processed for that second.
  The connector doesn’t remove duplicate `DELETE` events that are already in the `__EVENT_LOG` table.

## Version 5.28.3 (October 7, 2026)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue where the `CHECK_ROW_COUNT` procedure’s `max_sys_created_on` filter always reported a Snowflake row
  count of 0 if global display value fetching was enabled.

## Version 5.28.2 (September 11, 2026)

### Behavior changes

Not applicable.

### New features

Not applicable.

### Bug fixes

- Fixed an issue where calling the `CONFIGURE_SCAN_EVENT_LOG_IN_INCREMENTAL` stored procedure with `FALSE` didn’t
  reduce `__EVENT_LOG` table scanning during deletions synchronization the way it did for inserts and updates. On
  accounts with a large `__EVENT_LOG` table, this issue could cause the connector to scan the entire table for every
  batch of the deletions journal.
- Fixed an issue where the `CHECK_ROW_COUNT` procedure’s `max_sys_created_on` filter always reported a Snowflake row
  count of 0 for connectors that have display value fetching enabled.

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
