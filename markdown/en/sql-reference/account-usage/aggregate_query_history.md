Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# AGGREGATE\_QUERY\_HISTORY view

This Account Usage view enables you to monitor and track execution of statements
over time. It contains similar data to the QUERY\_HISTORY view but is aggregated
in one-minute intervals for repeated SQL statements. You can use this view to
monitor your workload and analyze performance.

In addition to queries against hybrid tables, all queries that you execute in
Snowflake are included in AGGREGATE\_QUERY\_HISTORY. However, AGGREGATE\_QUERY\_HISTORY
is particularly useful for monitoring and analyzing Unistore workloads
that execute a small number of distinct statements repeatedly at high throughput.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CALLS | NUMBER | Number of times the statement (query + query plan) was executed in the aggregation interval. |
| INTERVAL\_START\_TIME | TIMESTAMP\_LTZ | Start time of the window of measurement (in the local time zone). |
| INTERVAL\_END\_TIME | TIMESTAMP\_LTZ | End time of the window of measurement (in the local time zone). |
| QUERY\_PARAMETERIZED\_HASH | TEXT | Unique ID to identify identical parameterized queries. See [QUERY\_PARAMETERIZED\_HASH column](#label-hybrid-table-query-parameterized-hash). |
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
| BYTES\_WRITTEN | OBJECT | Number of bytes written (e.g. when loading into a table). |
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
| EXTERNAL\_FUNCTION\_TOTAL\_INVOCATIONS | OBJECT | Aggregate number of times that this query called remote services. For important details, see the Usage Notes. |
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

The OBJECT data type contains the following fields:

| Field Name | Description |
| --- | --- |
| [sum](/sql-reference/functions/sum) | Sum across all executions within the aggregation interval. |
| [avg](/sql-reference/functions/avg) | Average across all executions within the aggregation interval. |
| [stddev](/sql-reference/functions/stddev) | Standard deviation across all executions within the aggregation interval. |
| [min](/sql-reference/functions/min) | Minimum across all executions within the aggregation interval. |
| [median](/sql-reference/functions/median) | Median across all executions within the aggregation interval. |
| [p90](/sql-reference/functions/percentile_cont) | 90th percentile across all executions within the aggregation interval. |
| [p99](/sql-reference/functions/percentile_cont) | 99th percentile across all executions within the aggregation interval. |
| [p99.9](/sql-reference/functions/percentile_cont) | 99.9th percentile across all executions within the aggregation interval. |
| [max](/sql-reference/functions/max) | Maximum across all executions within the aggregation interval. |

Expand

Show lessSee more

Note

The following columns of the type OBJECT do not contain a `sum` field:

- PERCENTAGE\_SCANNED\_FROM\_CACHE
- QUERY\_LOAD\_PERCENT
- QUERY\_ACCELERATION\_UPPER\_LIMIT\_SCALE\_FACTOR

### QUERY\_PARAMETERIZED\_HASH column

The QUERY\_PARAMETERIZED\_HASH column contains a hash value that is computed based on the parameterized query, which means the version of the query after parameterizing all literals.

For example, the following queries have the same QUERY\_PARAMETERIZED\_HASH value:

Copy code

```
SELECT * FROM table1 WHERE table1.name = 'TIM'
```

Copy code

```
SELECT * FROM table1 WHERE table1.name = 'AIHUA'
```

The QUERY\_PARAMETERIZED\_HASH value has the following restrictions:

> - The constant literal must be in the following binary functions on predicates: equal, not equal, greater (or equal) than, smaller (or equal) than.
> - The aliases must be the same.

As long as there are difference in the SQL text, the QUERY\_HASH and QUERY\_PARAMETERIZED\_HASH values will be different, with the following exceptions:

> - Identifier/session variable/stage name are case insensitive.
> - White space differences are ignored.
> - Literals satisfying the binary predicate rule mentioned above.

## Usage notes

Latency for the view may be up to 180 minutes (3 hours).

## Examples

You can use the AGGREGATE\_QUERY\_HISTORY view to monitor for potential problems with errors, queueing, lock blocking, or hybrid table throttling.
You typically want these metrics to be consistently low. If you see a spike in any of these metrics, it may indicate a problem:

> Copy code
>
> ```
> SET (START_DATE, END_DATE) = ('2023-11-01', '2023-11-08');
>
> WITH time_issues AS
> (
>     SELECT
>         interval_start_time
>         , SUM(transaction_blocked_time:"sum") AS transaction_blocked_time
>         , SUM(queued_provisioning_time:"sum") AS queued_provisioning_time
>         , SUM(queued_repair_time:"sum") AS queued_repair_time
>         , SUM(queued_overload_time:"sum") AS queued_overload_time
>         , SUM(hybrid_table_requests_throttled_count) AS hybrid_table_requests_throttled_count
>     FROM snowflake.account_usage.aggregate_query_history
>     WHERE TRUE
>         AND interval_start_time > $START_DATE
>         AND interval_start_time < $END_DATE
>     GROUP BY ALL
> ),
> errors AS
> (
>     SELECT
>         interval_start_time
>         , SUM(value:"count") as error_count
>     FROM
>     (
>         SELECT
>             a.interval_start_time
>             , e.*
>         FROM
>             snowflake.account_usage.aggregate_query_history a,
>             TABLE(FLATTEN(input => errors)) e
>         WHERE TRUE
>             AND interval_start_time > $START_DATE
>             AND interval_start_time < $END_DATE
>     )
>     GROUP BY ALL
> )
> SELECT
>     time_issues.interval_start_time
>     , error_count
>     , transaction_blocked_time
>     , queued_provisioning_time
>     , queued_repair_time
>     , queued_overload_time
>     , hybrid_table_requests_throttled_count
> FROM
>     time_issues FULL JOIN errors ON errors.interval_start_time = time_issues.interval_start_time
> ;
> ```

You can query the view to monitor your overall workload throughput and concurrency. Many workloads have a regular cyclical pattern.
Any unexpected spikes or drops may be worth investigating.

For example, monitor throughput and concurrency for warehouse `my_warehouse` in the first week of November:

Copy code

```
SELECT
    interval_start_time
    , SUM(calls) AS execution_count
    , SUM(calls) / 60 AS queries_per_second
    , COUNT(DISTINCT session_id) AS unique_sessions
    , COUNT(user_name) AS unique_users
FROM snowflake.account_usage.aggregate_query_history
WHERE TRUE
    AND warehouse_name = 'MY_WAREHOUSE'
    AND interval_start_time > '2023-11-01'
    AND interval_start_time < '2023-11-08'
GROUP BY
    interval_start_time
;
```

The most common and heavily repeated queries can be a good place to focus any efforts to optimize or improve the efficiency of
your workload. You can query the view to identify top queries for a workload by execution count.

For example, identify the top queries by execution count for warehouse `my_warehouse`:

Copy code

```
SELECT
    query_parameterized_hash
    , ANY_VALUE(query_text)
    , SUM(calls) AS execution_count
FROM snowflake.account_usage.aggregate_query_history
WHERE TRUE
    AND warehouse_name = 'MY_WAREHOUSE'
    AND interval_start_time > '2023-11-01'
    AND interval_start_time < '2023-11-08'
GROUP BY
    query_parameterized_hash
ORDER BY execution_count DESC
;
```

To identify slowest queries by average total latency:

Copy code

```
SELECT
    query_parameterized_hash
    , any_value(query_text)
    , SUM(total_elapsed_time:"sum"::NUMBER) / SUM (calls) as avg_latency
FROM snowflake.account_usage.aggregate_query_history
WHERE TRUE
    AND warehouse_name = 'MY_WAREHOUSE'
    AND interval_start_time > '2023-07-01'
    AND interval_start_time < '2023-07-08'
GROUP BY
    query_parameterized_hash
ORDER BY avg_latency DESC
;
```

To analyze performance over time for a specific query of interest:

Copy code

```
SELECT
    interval_start_time
    , total_elapsed_time:"avg"::number avg_elapsed_time
    , total_elapsed_time:"min"::number min_elapsed_time
    , total_elapsed_time:"p90"::number p90_elapsed_time
    , total_elapsed_time:"p99"::number p99_elapsed_time
    , total_elapsed_time:"max"::number max_elapsed_time
FROM snowflake.account_usage.aggregate_query_history
WHERE TRUE
    AND query_parameterized_hash = '<123456>'
    AND interval_start_time > '2023-07-01'
    AND interval_start_time < '2023-07-08'
ORDER BY interval_start_time DESC
;
```
