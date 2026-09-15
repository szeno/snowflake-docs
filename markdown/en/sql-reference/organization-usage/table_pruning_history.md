[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# TABLE\_PRUNING\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to determine the efficiency of pruning for all tables,
and to understand how a table’s default (natural) ordering of data affects pruning.

You can compare the number of partitions pruned (`PARTITIONS_PRUNED`) to the
total number of partitions scanned and pruned (`PARTITIONS_SCANNED + PARTITIONS_PRUNED`).

Each row in this view represents the pruning history for a specific table within a given time interval.
The data is aggregated by time interval and includes information about the number of scans, partitions
scanned, partitions pruned, rows scanned, and rows pruned.

You can also use this view to compare the effects on pruning before and after enabling
[Automatic Clustering](/user-guide/tables-auto-reclustering) and
[search optimization](/user-guide/search-optimization-service) for a table.

See also [TABLE\_QUERY\_PRUNING\_HISTORY view](/sql-reference/organization-usage/table_query_pruning_history) and
[COLUMN\_QUERY\_PRUNING\_HISTORY view](/sql-reference/organization-usage/column_query_pruning_history).

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the time range (on the hour mark) during which the queries were executed and completed. |
| END\_TIME | TIMESTAMP\_LTZ | End of the time range (on the hour mark) during which the queries were executed and completed. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table that was queried. |
| TABLE\_NAME | VARCHAR | Name of the table that was queried. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table that was queried. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table that was queried. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table that was queried. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table that was queried. |
| NUM\_SCANS | NUMBER | Number of scan operations from all queries (including SELECT statements and DML statements) on the table during the START\_TIME and END\_TIME window. Note that a given query might result in multiple scan operations on the same table. |
| PARTITIONS\_SCANNED | NUMBER | Number of partitions scanned during the scan operations described in `NUM_SCANS`. |
| PARTITIONS\_PRUNED | NUMBER | Number of partitions pruned for the queries described in `NUM_SCANS`. These partitions were eliminated during query processing, improving the efficiency of the query. |
| ROWS\_SCANNED | NUMBER | Number of rows scanned during the scan operations described in `NUM_SCANS`. |
| ROWS\_PRUNED | NUMBER | Number of rows pruned for the queries described in `NUM_SCANS`. These rows were eliminated during query processing, improving the efficiency of the query. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 8 hours.
- This view does not include pruning information for [hybrid tables](/user-guide/tables-hybrid).
- This view retains data for the 1,000 longest-running table scans per query. Only extremely complex queries
  exceed this number of scans so data is rarely omitted.
