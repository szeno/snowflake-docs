[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# DYNAMIC\_TABLE\_REFRESH\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays information for dynamic table refresh history.

See also:
:   [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) (Information Schema)

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
| NAME | VARCHAR | Name of the dynamic table. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the dynamic table. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the dynamic table. |
| ID | NUMBER | Internal, Snowflake-generated identifier for the dynamic table. |
| SCHEMA\_ID | NUMBER | Internal, Snowflake-generated identifier of the schema that contains the dynamic table. |
| DATABASE\_ID | NUMBER | Internal, Snowflake-generated identifier of the database that contains the dynamic table. |
| STATE | VARCHAR | Status of the refresh for the dynamic table. This can be one of the following:   - EXECUTING: refresh in progress.   - SUCCEEDED: refresh completed successfully.   - FAILED: refresh failed during execution.   - CANCELLED: refresh was canceled before execution.   - UPSTREAM\_FAILED: refresh not performed due to an upstream failed refresh. |
| STATE\_CODE | VARCHAR | Code representing the current state of the refresh. |
| STATE\_MESSAGE | VARCHAR | Description of the current state of the refresh. |
| QUERY\_ID | VARCHAR | ID of the SQL statement that produced the results for the dynamic table. |
| DATA\_TIMESTAMP | TIMESTAMP\_LTZ | Transactional timestamp when the refresh was evaluated. (This might be slightly before the actual time of the refresh.) All data, in base objects, that arrived before this timestamp is currently included in the dynamic table. |
| REFRESH\_START\_TIME | TIMESTAMP\_LTZ | Time when the refresh job started. |
| REFRESH\_END\_TIME | TIMESTAMP\_LTZ | Time when the refresh completed. |
| COMPLETION\_TARGET | TIMESTAMP\_LTZ | Time by which this refresh should complete to keep lag under the TARGET\_LAG parameter for the dynamic table. This is equal to the DATA\_TIMESTAMP of the last refresh + TARGET\_LAG. |
| QUALIFIED\_NAME | VARCHAR | Fully qualified name of the dynamic table as it appears in the graph of dynamic tables. You can use this to join the output with the output of the [DYNAMIC\_TABLE\_GRAPH\_HISTORY](/sql-reference/functions/dynamic_table_graph_history) function. |
| LAST\_COMPLETED\_DEPENDENCY | OBJECT | Contains the following properties:   - `qualified_name`: The qualified name of the latest dependency to become available.   - `data_timestamp`: The refresh version of that dependency. |
| STATISTICS | OBJECT | Contains the following properties:   - `numInsertedRows`: The number of inserted rows.   - `numDeletedRows`: The number of rows that were deleted.   - `numCopiedRows`: The number of rows that were copied unchanged.   - `numAddedPartitions`: The number of added partitions.   - `numRemovedPartitions` : The number of removed partitions.   - `queuedTimeMs`: The time (in milliseconds) spent in the queued state.   - `compilationTimeMs`: The time (in milliseconds) spent compiling the refresh query.   - `executionTimeMs`: The time (in milliseconds) spent executing the refresh query.   For successful refreshes, this column includes both the row/partition statistics and the time distribution information. For failed refreshes, this column is populated with the time distribution information only.   For example: If an UPDATE statement updates 1 row in a partition with 10 rows. Then the metrics above show 1 row inserted, 1 deleted, and 9 copied. Additionally, 1 partition is removed and 1 partition added. |
| REFRESH\_ACTION | VARCHAR | One of:   - NO\_DATA - no new data in base tables. Doesn’t apply to the initial refresh of newly created dynamic tables regardless of whether or not the base tables have data.   - REINITIALIZE - base table changed, source table of a cloned dynamic table was refreshed during clone, or an ADAPTIVE dynamic table chose to reinitialize because processing changes incrementally would be more expensive.   - FULL - Full refresh, because dynamic table contains query elements that are not incrementalizable (see SHOW DYNAMIC TABLE refresh\_mode\_reason) or because full refresh was cheaper than incremental refresh.   - INCREMENTAL - normal incremental refresh.   - CUSTOM\_INCREMENTAL - refresh performed using a user-defined custom incremental refresh handler. |
| REFRESH\_TRIGGER | VARCHAR | One of:   - SCHEDULED - normal background refresh to meet target lag or downstream target lag.   - MANUAL - user/task used ALTER DYNAMIC TABLE <name> REFRESH   - CREATION - refresh performed during the creation DDL statement, triggered by the creation of the dynamic table or any consumer dynamic tables. |
| TARGET\_LAG\_SEC | NUMBER | Describes the target lag for the dynamic tables at the time the refresh occurred. |
| GRAPH\_HISTORY\_VALID\_FROM | TIMESTAMP\_NTZ | Encodes the VALID\_FROM timestamp of the DYNAMIC\_TABLE\_GRAPH\_HISTORY table function when the refresh occurred to clarify which version of a dynamic table a specific refresh corresponds to. This value can also be NULL if the corresponding dynamic table hasn’t been created. |
| WAREHOUSE | VARCHAR | Warehouse used for the dynamic table refresh. |
| EXECUTE\_AS\_USER | VARCHAR | The user that the dynamic table refresh runs as. |
| SECONDARY\_ROLE\_NAMES | VARCHAR | The secondary roles used during dynamic table refresh execution. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 5 hours.
