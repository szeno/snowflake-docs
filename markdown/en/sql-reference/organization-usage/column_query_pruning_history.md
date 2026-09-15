[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# COLUMN\_QUERY\_PRUNING\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

Use this Organization Usage view to gain a better understanding of data access patterns during
query execution, including some column-level details, such as the “access type” and candidate
[search optimization expressions](/user-guide/search-optimization-service) that are potentially beneficial.

You can use this view in combination with the [TABLE\_QUERY\_PRUNING\_HISTORY view](/sql-reference/organization-usage/table_query_pruning_history). For example,
you can identify access to target tables by using the TABLE\_QUERY\_PRUNING\_HISTORY view, then
identify frequently used columns on those tables by using the COLUMN\_QUERY\_PRUNING\_HISTORY view.

Each row in this view represents the query pruning history for a specific column within a given time interval. The data is
aggregated per column, per table, per interval, and includes metrics such as the number of queries executed, partitions scanned,
partitions pruned, rows scanned, rows pruned, and rows matched.

See also [TABLE\_PRUNING\_HISTORY view](/sql-reference/organization-usage/table_pruning_history) and [Query Pruning](/user-guide/tables-clustering-micropartitions#label-micropartitions-query-pruning).

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
| INTERVAL\_START\_TIME | TIMESTAMP\_LTZ | Start of the time range (on the hour mark) during which the queries were executed and completed. |
| INTERVAL\_END\_TIME | TIMESTAMP\_LTZ | End of the time range (on the hour mark) during which the queries were executed and completed. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table that was queried. |
| TABLE\_NAME | VARCHAR | Name of the table that was queried. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table that was queried. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table that was queried. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table that was queried. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table that was queried. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse that was used to run the queries. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse that ran the queries. |
| QUERY\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-hash) computed based on the canonicalized SQL text. |
| QUERY\_PARAMETERIZED\_HASH | VARCHAR | The [hash value](/user-guide/query-hash#label-query-parameterized-hash) computed based on the parameterized query. |
| COLUMN\_ID | NUMBER | Internal/system-generated identifier for the column accessed from the table that was queried. |
| COLUMN\_NAME | VARCHAR | Name of the column accessed from the table that was queried. |
| VARIANT\_PATH | VARCHAR | Path to the semi-structured data being accessed (if applicable). NULL if the column accessed does not have a semi-structured data type. |
| ACCESS\_TYPE | VARCHAR | Type of access performed on the column (`WHERE` or `JOIN` condition). |
| NUM\_QUERIES | NUMBER | Number of queries executed in this time range with this specific QUERY\_HASH value, using this warehouse, accessing this column (and variant path if applicable) on this table with this type of access. |
| AGGREGATE\_QUERY\_ELAPSED\_TIME | NUMBER | Total elapsed time (in milliseconds) for queries defined by NUM\_QUERIES. This total includes queueing and other time not associated with compilation and execution. |
| AGGREGATE\_QUERY\_COMPILATION\_TIME | NUMBER | Total compilation time (in milliseconds) for queries defined by NUM\_QUERIES. |
| AGGREGATE\_QUERY\_EXECUTION\_TIME | NUMBER | Total execution time (in milliseconds) for queries defined by NUM\_QUERIES. |
| PARTITIONS\_SCANNED | NUMBER | Number of partitions scanned on this table for queries defined by NUM\_QUERIES. |
| PARTITIONS\_PRUNED | NUMBER | Number of partitions pruned on this table for queries defined by NUM\_QUERIES. These partitions were eliminated during query processing and not scanned, improving the efficiency of the query. |
| ROWS\_SCANNED | NUMBER | Number of rows scanned on this table for queries defined by NUM\_QUERIES. |
| ROWS\_PRUNED | NUMBER | Number of rows pruned on this table for queries defined by NUM\_QUERIES. These rows were eliminated during query processing and not scanned, improving the efficiency of the query. |
| ROWS\_MATCHED | NUMBER | Number of rows that matched the WHERE clause filters while scanning this table for the queries defined by NUM\_QUERIES. |
| SEARCH\_OPTIMIZATION\_SUPPORTED\_EXPRESSIONS | ARRAY | List of supported search optimization expressions on this column that could potentially speed up scanning this table for the queries defined by NUM\_QUERIES. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 6 hours.
- Data is retained for 1 year.
- This view does not include pruning information for [hybrid tables](/user-guide/tables-hybrid).
- The ACCESS\_TYPE column contains one of the following values:

  - `WHERE`: The column is used in a filter condition in the [WHERE](/sql-reference/constructs/where) clause.
  - `JOIN`: The column is used in a condition for a [JOIN](/sql-reference/constructs/join) operation.
- The access behavior shown in this view reflects the actual query plan that was executed, which might be different from the original query text. For example, if a HAVING clause does not reference aggregated results produced by the GROUP BY clause, it might be optimized and rewritten as a WHERE clause, and the ACCESS\_TYPE value will be `WHERE`.
- For complex filtering conditions that can’t benefit from a pushdown optimization, rows might not be filtered out during the table scan operation, even if they do not match the filtering condition. Therefore, these rows are counted in the ROWS\_MATCHED value.
- Currently, the SEARCH\_OPTIMIZATION\_SUPPORTED\_EXPRESSIONS column only suggests the EQUALITY and SUBSTRING [search methods](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction).
- This view retains data for the 1,000 longest-running table scans per query. Only extremely complex queries
  exceed this number of scans so data is rarely omitted.
