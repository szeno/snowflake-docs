Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# AGGREGATE\_QUERY\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view enables you to monitor and track the execution of statements over time across the accounts in your organization. It contains similar data to the [QUERY\_HISTORY view](/sql-reference/organization-usage/query_history) but is aggregated in one-minute intervals for repeated SQL statements.

This view contains the same data as the [AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history) in the ACCOUNT\_USAGE schema, additionally aggregated at the organization level. For details about how the data is aggregated, the fields returned by the OBJECT columns, and example queries, see the [AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history) in the ACCOUNT\_USAGE schema.

This view is available only in the [organization account](/user-guide/organization-accounts). Users with the GLOBALORGADMIN role, or users granted the SNOWFLAKE.ORGANIZATION\_GOVERNANCE\_VIEWER application role, can access it. For details, see [Accessing the ORGANIZATION\_USAGE schema](/sql-reference/organization-usage#label-org-usage-access-org-account).

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
| CALLS | NUMBER | Number of times the statement (query + query plan) was executed in the aggregation interval. |
| INTERVAL\_START\_TIME | TIMESTAMP\_LTZ | Start time of the window of measurement (in the local time zone). |
| INTERVAL\_END\_TIME | TIMESTAMP\_LTZ | End time of the window of measurement (in the local time zone). |
| QUERY\_PARAMETERIZED\_HASH | TEXT | Unique ID to identify identical parameterized queries. See [QUERY\_PARAMETERIZED\_HASH column](/sql-reference/account-usage/aggregate_query_history#label-hybrid-table-query-parameterized-hash). |
| QUERY\_TEXT | TEXT | Sample text of the SQL statement. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that was in use. |
| DATABASE\_NAME | TEXT | Database that was in use at the time of the query. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that was in use. |
| SCHEMA\_NAME | TEXT | Schema that was in use at the time of the query. |
| QUERY\_TYPE | TEXT | DML, query, etc. If the query failed, then the query type may be UNKNOWN. |
| SESSION\_ID | NUMBER | Session that executed the statement. |
| USER\_NAME | TEXT | User who issued the query. |
| ROLE\_NAME | TEXT | Role that was active in the session at the time of the query. |
| ROLE\_TYPE | TEXT | Specifies `APPLICATION`, `DATABASE_ROLE`, or `ROLE` that executed the query. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse that was used. |
| WAREHOUSE\_NAME | TEXT | Warehouse that the query executed on, if any. |
| WAREHOUSE\_SIZE | TEXT | Size of the warehouse when this statement executed. |
| WAREHOUSE\_TYPE | TEXT | Type of the warehouse when this statement executed. |
| QUERY\_TAG | TEXT | Query tag set for this statement through the QUERY\_TAG session parameter. |
| IS\_CLIENT\_GENERATED\_STATEMENT | BOOLEAN | Indicates whether the query was client-generated. |
| RELEASE\_VERSION | TEXT | Release version in the format of `major_release.minor_release.patch_release`. |
| ERRORS | ARRAY | List of error codes and messages that occurred during the aggregation interval. Each error is in the format of `{"code": "code1", "message": "msg1", "count": 10}`. |
| TOTAL\_ELAPSED\_TIME | OBJECT | Elapsed time (in milliseconds). |
| BYTES\_SCANNED | OBJECT | Number of bytes scanned by this statement. |
| PERCENTAGE\_SCANNED\_FROM\_CACHE | OBJECT | The percentage of data scanned from the local disk cache. The value ranges from 0.0 to 1.0. Multiply by 100 to get a true percentage. |
| BYTES\_WRITTEN | OBJECT | Number of bytes written (for example, when loading into a table). |
| BYTES\_WRITTEN\_TO\_RESULT | OBJECT | Number of bytes written to a result object. For example, `select * from . . .` would produce a set of results in tabular format representing each field in the selection.     In general, the results object represents whatever is produced as a result of the query, and `BYTES_WRITTEN_TO_RESULT` represents the size of the returned result. |
| BYTES\_READ\_FROM\_RESULT | OBJECT | Number of bytes read from a result object. |
| ROWS\_PRODUCED | OBJECT | Number of rows produced by this statement. |
| ROWS\_INSERTED | OBJECT | Number of rows inserted by the query. |
| ROWS\_UPDATED | OBJECT | Number of rows updated by the query. |
| ROWS\_DELETED | OBJECT | Number of rows deleted by the query. |
| ROWS\_UNLOADED | OBJECT | Number of rows unloaded during data export. |
| BYTES\_DELETED | OBJECT | Number of bytes deleted by the query. |
| PARTITIONS\_SCANNED | OBJECT | Number of micro-partitions scanned. |
| PARTITIONS\_TOTAL | OBJECT | Total micro-partitions of all tables included in this query. |
| BYTES\_SPILLED\_TO\_LOCAL\_STORAGE | OBJECT | Volume of data spilled to local disk. |
| BYTES\_SPILLED\_TO\_REMOTE\_STORAGE | OBJECT | Volume of data spilled to remote disk. |
| BYTES\_SENT\_OVER\_THE\_NETWORK | OBJECT | Volume of data sent over the network. |
| COMPILATION\_TIME | OBJECT | Compilation time (in milliseconds). |
| EXECUTION\_TIME | OBJECT | Execution time (in milliseconds). |
| QUEUED\_PROVISIONING\_TIME | OBJECT | Time (in milliseconds) spent in the warehouse queue, waiting for the warehouse compute resources to provision, due to warehouse creation, resume, or resize. |
| QUEUED\_REPAIR\_TIME | OBJECT | Time (in milliseconds) spent in the warehouse queue, waiting for compute resources in the warehouse to be repaired. |
| QUEUED\_OVERLOAD\_TIME | OBJECT | Time (in milliseconds) spent in the warehouse queue, due to the warehouse being overloaded by the current query workload. |
| TRANSACTION\_BLOCKED\_TIME | OBJECT | Time (in milliseconds) spent blocked by a concurrent DML. |
| OUTBOUND\_DATA\_TRANSFER\_CLOUD | TEXT | Target cloud provider for statements that unload data to another region and/or cloud. |
| OUTBOUND\_DATA\_TRANSFER\_REGION | TEXT | Target region for statements that unload data to another region and/or cloud. |
| OUTBOUND\_DATA\_TRANSFER\_BYTES | OBJECT | Number of bytes transferred in statements that unload data to another region and/or cloud. |
| INBOUND\_DATA\_TRANSFER\_CLOUD | TEXT | Source cloud provider for statements that load data from another region and/or cloud. |
| INBOUND\_DATA\_TRANSFER\_REGION | TEXT | Source region for statements that load data from another region and/or cloud. |
| INBOUND\_DATA\_TRANSFER\_BYTES | OBJECT | Number of bytes transferred in a replication operation from another account. The source account could be in the same region or a different region than the current account. |
| LIST\_EXTERNAL\_FILES\_TIME | OBJECT | Time (in milliseconds) spent listing external files. |
| CREDITS\_USED\_CLOUD\_SERVICES | OBJECT | Number of credits used for cloud services. |
| EXTERNAL\_FUNCTION\_TOTAL\_INVOCATIONS | OBJECT | Aggregate number of times that this query called remote services. |
| EXTERNAL\_FUNCTION\_TOTAL\_SENT\_ROWS | OBJECT | Total number of rows that this query sent in all calls to all remote services. |
| EXTERNAL\_FUNCTION\_TOTAL\_RECEIVED\_ROWS | OBJECT | Total number of rows that this query received from all calls to all remote services. |
| EXTERNAL\_FUNCTION\_TOTAL\_SENT\_BYTES | OBJECT | Total number of bytes that this query sent in all calls to all remote services. |
| EXTERNAL\_FUNCTION\_TOTAL\_RECEIVED\_BYTES | OBJECT | Total number of bytes that this query received from all calls to all remote services. |
| QUERY\_LOAD\_PERCENT | OBJECT | The approximate percentage of active compute resources in the warehouse for this query execution. |
| QUERY\_ACCELERATION\_BYTES\_SCANNED | OBJECT | Number of bytes scanned by the [query acceleration service](/user-guide/query-acceleration-service). |
| QUERY\_ACCELERATION\_PARTITIONS\_SCANNED | OBJECT | Number of partitions scanned by the query acceleration service. |
| QUERY\_ACCELERATION\_UPPER\_LIMIT\_SCALE\_FACTOR | OBJECT | Upper limit [scale factor](/user-guide/query-acceleration-service#label-query-acceleration-scale-factor) that a [query would have benefited from](/user-guide/query-acceleration-service). |
| CHILD\_QUERIES\_WAIT\_TIME | OBJECT | Time (in milliseconds) to complete the cached lookup when calling a [memoizable function](/developer-guide/udf/sql/udf-sql-scalar-functions#label-udf-sql-scalar-memoizable). |
| HYBRID\_TABLE\_REQUESTS\_THROTTLED\_COUNT | NUMBER | Number of hybrid table queries that were throttled. |

Expand

Show lessSee more

For columns with the OBJECT data type, the object contains statistical fields (such as `sum`, `avg`, and percentiles) computed across all executions within the aggregation interval. For a description of these fields, see the [AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history) in the ACCOUNT\_USAGE schema.

## Usage notes

- Latency for the view may be up to 300 minutes (5 hours).
- The data is retained for 365 days (1 year).

## Examples

For example queries, see the [AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history#examples) in the ACCOUNT\_USAGE schema. To find organization-level information, replace `SNOWFLAKE.ACCOUNT_USAGE` with `SNOWFLAKE.ORGANIZATION_USAGE` in the queries.
