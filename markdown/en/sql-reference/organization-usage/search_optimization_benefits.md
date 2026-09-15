[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SEARCH\_OPTIMIZATION\_BENEFITS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to determine the efficacy of pruning due to
[search optimization](/user-guide/search-optimization-service).

This view provides information about pruning, similar to the information provided by the [TABLE\_PRUNING\_HISTORY view](/sql-reference/organization-usage/table_pruning_history). Note that
TABLE\_PRUNING\_HISTORY view provides information about all pruning, as opposed to pruning due to search optimization.

You can use this view to compare the effects on pruning before and after adding search optimization to a table. When you query
this view, compare the number of partitions pruned due to search optimization (`PARTITIONS_PRUNED_ADDITIONAL`) against the
total number of partitions pruned (`PARTITIONS_PRUNED_DEFAULT + PARTITIONS_PRUNED_ADDITIONAL`).

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
| START\_TIME | TIMESTAMP\_LTZ | Start of the time range (on the hour mark) during which the queries were executed. |
| END\_TIME | TIMESTAMP\_LTZ | End of the time range (on the hour mark) during which the queries were executed. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table that was queried. |
| TABLE\_NAME | VARCHAR | Name of the table that was queried. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table that was queried. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table that was queried. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table that was queried. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table that was queried. |
| NUM\_SCANS | NUMBER | Number of scan operations (from all queries on the table during the START\_TIME and END\_TIME window) that used [search optimization](/user-guide/search-optimization-service) to improve pruning. Note that a given query might result in multiple scan operations on the same table. |
| PARTITIONS\_SCANNED | NUMBER | Number of partitions scanned during the scan operations described in `NUM_SCANS`. |
| PARTITIONS\_PRUNED\_DEFAULT | NUMBER | Number of partitions that were pruned as a result of the default (natural) ordering of data for the queries described in `NUM_SCANS`. These partitions were eliminated during query processing, improving the efficiency of the query. |
| PARTITIONS\_PRUNED\_ADDITIONAL | NUMBER | Number of partitions that were pruned as a result of [search optimization](/user-guide/search-optimization-service) for the queries described in `NUM_SCANS`. These partitions were eliminated during query processing, improving the efficiency of the query. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 8 hours.
- This view retains data for the 1,000 longest-running table scans per query. Only extremely complex queries
  exceed this number of scans so data is rarely omitted.
