# Snowflake Connector for ServiceNow® V2 release notes for 2026

This topic provides release notes for the Snowflake Connector for ServiceNow® V2. For additional
information, see
[Snowflake Connector for ServiceNow](https://other-docs.snowflake.com/en/connectors/servicenow/v2/about).

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
