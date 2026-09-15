Categories:
:   [System functions](/sql-reference/functions-system) (Query Information) ,
    [Table functions](/sql-reference/functions-table)

# GET\_QUERY\_OPERATOR\_STATS

Returns statistics about individual query operators within a query that has completed. You can run this function for any
completed query that was executed in the past 14 days.

You can use this information to understand the structure of a query and identify query operators — for example, the join operator —
that cause performance problems.

For example, you can use this information to determine which operators are consuming the most resources. As another example, you
can use this function to identify joins that have more output rows than input rows, which can be a sign of an
[“exploding” join](/user-guide/ui-snowsight-activity#label-exploding-join); for example, an unintended Cartesian product.

These statistics are also available in the [query profile](/user-guide/ui-snowsight-activity#label-snowsight-query-profile) tab in Snowsight.
The `GET_QUERY_OPERATOR_STATS()` function makes the same information available via a programmatic interface.

For more information about finding problematic query operators,
see [Common query problems identified by Query Profile](/user-guide/ui-snowsight-activity#label-common-query-problems-identified-by-query-profile).

## Syntax

Copy code

```
GET_QUERY_OPERATOR_STATS( <query_id> )
```

## Arguments

`query_id`
:   The ID of a query. You can use:

    - A string literal (a string surrounded by single quotes).
    - A [session variable](/sql-reference/session-variables) containing a query ID.
    - The return value from a call to the [LAST\_QUERY\_ID](/sql-reference/functions/last_query_id) function.

## Returns

The GET\_QUERY\_OPERATOR\_STATS function is a [table function](/sql-reference/functions-table). It returns rows with
statistics about each query operator in the query. For more information, see the
[Usage notes](#label-get-query-operator-stats-usage-notes) and [Output](#label-get-query-operator-stats-output) sections below.

## Usage notes

- This function returns statistics only for queries that have completed.
- You must have OPERATE or MONITOR privileges on the warehouse where you ran the query.
- This function provides detailed statistics about each query operator used in the specified query. The following list
  shows the possible query operators:

  - Aggregate: Groups inputs and computes aggregate functions.
  - CartesianJoin: A specialized type of join.
  - Delete: Removes a record from a table.
  - ExternalFunction: Represents processing by an external function.
  - ExternalScan: Represents access to data stored in stage objects.
  - Filter: Represents an operation that filters the rows.
  - Flatten: Processes VARIANT records, possibly flattening them on a specified path.
  - Generator: Generates records by using the TABLE([GENERATOR(…)](/sql-reference/functions/generator)) construct.
  - GroupingSets: Represents constructs, such as GROUPING SETS, ROLLUP, and CUBE.
  - Insert: Adds a record to a table either through an INSERT or COPY operation.
  - InternalObject: Represents access to an internal data object; for example, in an [Information Schema](/sql-reference/info-schema)
    or the result of a previous query.
  - Join: Combines two inputs on a given condition.
  - JoinFilter: Special filtering operation that removes tuples that can be identified as not possibly matching the condition of a
    Join further in the query plan.
  - Merge: Performs a MERGE operation on a table.
  - Pivot: Transforms unique values from a column into multiple columns and does any necessary aggregation.
  - Result: Returns the query result.
  - Sort: Orders input on a given expression.
  - SortWithLimit: Produces a part of the input sequence after sorting, typically a result of an
    `ORDER BY ... LIMIT ... OFFSET ...` construct.
  - TableScan: Represents access to a single table.
  - UnionAll: Concatenates two inputs.
  - Unload: Represents a COPY operation that exports data from a table to a file in a stage.
  - Unpivot: Rotates a table by transforming columns into rows.
  - Update: Updates a record in a table.
  - ValuesClause: List of values provided with the VALUES clause.
  - WindowFunction: Computes window functions.
  - WithClause: Precedes the body of the SELECT statement, and defines one or more CTEs.
  - WithReference: Instance of a WITH clause.
- The information is returned as a table. Each row in the table corresponds to one operator. The row contains the execution
  breakdown and the query statistics for that operator.

  The row may also list [operator attributes](#label-get-query-operator-stats-operator-attributes) (these depend on the
  type of operator).

  Statistics that break down query execution time are expressed as a percentage of the total query execution time.

  For more information about specific statistics, see [Output](#label-get-query-operator-stats-output) (in this topic).
- Because this function is a table function, you must use it in a [FROM](/sql-reference/constructs/from) clause and you must wrap
  it in `TABLE()`. For example:

  Copy code

  ```
  SELECT * FROM TABLE(GET_QUERY_OPERATOR_STATS(last_query_id()));
  ```

- For each individual execution of a specific query (i.e. a specific UUID), this function is deterministic; it returns the same
  values each time.

  However, for different executions of the same query text, this function can return different runtime statistics. The statistics
  depend on many factors. The following factors can have a major impact on the execution and therefore on the statistics returned by
  this function:

  - The volume of data.
  - The availability of [materialized views](/user-guide/views-materialized), and the changes (if any) to the data since
    those materialized views were last refreshed.
  - The presence or absence of [clustering](/user-guide/tables-clustering-keys).
  - The presence or absence of previously-cached data.
  - The size of the virtual warehouse.

  The values can also be affected by factors outside the user’s query and data. These factors are usually small. The factors
  include:

  - Virtual warehouse initialization time.
  - Latency with external functions.

## Output

The function returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| QUERY\_ID | VARCHAR | The query ID, which is an internal, system-generated identifier for the SQL statement. |
| STEP\_ID | NUMBER(38, 0) | Identifier of the step in the query plan. |
| OPERATOR\_ID | NUMBER(38, 0) | The operator’s identifier. This is unique within the query. Values start at 0. |
| PARENT\_OPERATORS | ARRAY containing one or more NUMBER(38, 0) | Identifiers of the parent operators for this operator, or NULL if this is the final operator in the query plan (which is usually the Result operator). |
| OPERATOR\_TYPE | VARCHAR | The type of query operator; for example, `TableScan` or `Filter`. |
| [OPERATOR\_STATISTICS](#label-get-query-operator-stats-operator-statistics) | VARIANT containing an OBJECT | Statistics about the operator (for example, the number of output rows from the operator). |
| [EXECUTION\_TIME\_BREAKDOWN](#label-get-query-operator-stats-execution-time-breakdown) | VARIANT containing an OBJECT | Information about the execution time of the operator. |
| [OPERATOR\_ATTRIBUTES](#label-get-query-operator-stats-operator-attributes) | VARIANT containing an OBJECT | Information about the operator. This information depends on the operator type. |

Expand

Show lessSee more

If there is no information for the specific column for the operator, the value is NULL.

Three of these columns contain [OBJECTs](/sql-reference/data-types-semistructured#label-data-type-object). Each object contains key/value pairs. The tables below
describe the keys in these objects.

### OPERATOR\_STATISTICS

The fields in the OBJECTs for the `OPERATOR_STATISTICS` column provide additional information about the operator. The
information can include:

| Key | Nested key (if applicable) | Data type | Description |
| --- | --- | --- | --- |
| `dml` |  |  | Statistics for Data Manipulation Language (DML) queries. |
|  | `number_of_rows_inserted` | DOUBLE | Number of rows inserted into a table or tables. |
|  | `number_of_rows_updated` | DOUBLE | Number of rows updated in a table. |
|  | `number_of_rows_deleted` | DOUBLE | Number of rows deleted from a table. |
|  | `number_of_rows_unloaded` | DOUBLE | Number of rows unloaded during data export. |
| `extension_functions` |  |  | Information about calls to extension functions. If the value of a field is zero, then the field is not displayed. |
|  | `Java UDF handler load time` | DOUBLE | Amount of time for the Java UDF handler to load. |
|  | `Total Java UDF handler invocations` | DOUBLE | Number of times the Java UDF handler is invoked. |
|  | `Max Java UDF handler execution time` | DOUBLE | Maximum amount of time for the Java UDF handler to execute. |
|  | `Avg Java UDF handler execution time` | DOUBLE | Average amount of time to execute the Java UDF handler. |
|  | `Java UDTF process() invocations` | DOUBLE | Number of times the Java UDTF [process method](/developer-guide/udf/java/udf-java-tabular-functions#label-udf-java-methods) was invoked. |
|  | `Java UDTF process() execution time` | DOUBLE | Amount of time to execute the Java UDTF process. |
|  | `Avg Java UDTF process() execution time` | DOUBLE | Average amount of time to execute the Java UDTF process. |
|  | `Java UDTF's constructor invocations` | DOUBLE | Number of times the Java UDTF [constructor](/developer-guide/udf/java/udf-java-tabular-functions#label-udf-java-methods) was invoked. |
|  | `Java UDTF's constructor execution time` | DOUBLE | Amount of time to execute the Java UDTF constructor. |
|  | `Avg Java UDTF's constructor execution time` | DOUBLE | Average amount of time to execute the Java UDTF constructor. |
|  | `Java UDTF endPartition() invocations` | DOUBLE | Number of times the Java UDTF [endPartition method](/developer-guide/udf/java/udf-java-tabular-functions#label-udf-java-methods) was invoked. |
|  | `Java UDTF endPartition() execution time` | DOUBLE | Amount of time to execute the Java UDTF endPartition method. |
|  | `Avg Java UDTF endPartition() execution time` | DOUBLE | Average amount of time to execute the Java UDTF `endPartition` method. |
|  | `Max Java UDF dependency download time` | DOUBLE | Maximum amount of time to download the Java UDF dependencies. |
|  | `Max JVM memory usage` | DOUBLE | Peak memory usage as reported by the JVM. |
|  | `Java UDF inline code compile time in ms` | DOUBLE | Compile time for the Java UDF inline code. |
|  | `Total Python UDF handler invocations` | DOUBLE | Number of times the Python UDF handler was invoked. |
|  | `Total Python UDF handler execution time` | DOUBLE | Total execution time for the Python UDF handler. |
|  | `Avg Python UDF handler execution time` | DOUBLE | Average amount of time to execute the Python UDF handler. |
|  | `Python sandbox max memory usage` | DOUBLE | Peak memory usage by the Python sandbox environment. |
|  | `Avg Python env creation time: Download and install packages` | DOUBLE | Average amount of time to create the Python environment, including downloading and installing packages. |
|  | `Conda solver time` | DOUBLE | Amount of time to run the Conda solver to solve Python packages. |
|  | `Conda env creation time` | DOUBLE | Amount of time to create the Python environment. |
|  | `Python UDF initialization time` | DOUBLE | Amount of time to initialize the Python UDF. |
|  | `Number of external file bytes read for UDFs` | DOUBLE | Number of external file bytes read for UDFs. |
|  | `Number of external files accessed for UDFs` | DOUBLE | Number of external files accessed for UDFs. |
| `external_functions` |  |  | Information about calls to external functions. If the value of a field — for example `retries_due_to_transient_errors` — is zero, then the field is not displayed. |
|  | `total_invocations` | DOUBLE | Number of times that an external function was called. This number can be different from the number of external function calls in the text of the SQL statement because of the number of batches that rows are divided into, the number of retries if there are transient network problems, and so on. |
|  | `rows_sent` | DOUBLE | Number of rows sent to external functions. |
|  | `rows_received` | DOUBLE | Number of rows received back from external functions. |
|  | `bytes_sent (x-region)` | DOUBLE | Number of bytes sent to external functions. If the key includes `(x-region)`, the data was sent across regions, which can impact billing. |
|  | `bytes_received (x-region)` | DOUBLE | Number of bytes received from external functions. If the key includes `(x-region)`, the data was sent across regions, which can impact billing. |
|  | `retries_due_to_transient_errors` | DOUBLE | Number of retries because of transient errors. |
|  | `average_latency_per_call` | DOUBLE | Average amount of time per invocation (call) in milliseconds between the time Snowflake sent the data and received the returned data. |
|  | `http_4xx_errors` | INTEGER | Total number of HTTP requests that returned a 4xx status code. |
|  | `http_5xx_errors` | INTEGER | Total number of HTTP requests that returned a 5xx status code. |
|  | `average_latency` | DOUBLE | Average latency for successful HTTP requests. |
|  | `avg_throttle_latency_overhead` | DOUBLE | Average overhead per successful request because of a slowdown caused by throttling (HTTP 429). |
|  | `batches_retried_due_to_throttling` | DOUBLE | Number of batches that were retried because of HTTP 429 errors. |
|  | `latency_per_successful_call_(p50)` | DOUBLE | 50th percentile latency for successful HTTP requests. 50 percent of all successful requests took less than this time to complete. |
|  | `latency_per_successful_call_(p90)` | DOUBLE | 90th percentile latency for successful HTTP requests. 90 percent of all successful requests took less than this time to complete. |
|  | `latency_per_successful_call_(p95)` | DOUBLE | 95th percentile latency for successful HTTP requests. 95 percent of all successful requests took less than this time to complete. |
|  | `latency_per_successful_call_(p99)` | DOUBLE | 99th percentile latency for successful HTTP requests. 99 percent of all successful requests took less than this time to complete. |
| `input_rows` |  | INTEGER | Number of input rows. This can be missing for an operator with no input edges from other operators. |
| `io` |  |  | Information about the I/O (input/output) operations performed during the query. |
|  | `scan_progress` | DOUBLE | Percentage of data scanned for a given table so far. |
|  | `bytes_scanned` | DOUBLE | Number of bytes scanned so far. |
|  | `percentage_scanned_from_cache` | DOUBLE | Percentage of data scanned from the local disk cache. |
|  | `bytes_written` | DOUBLE | Bytes written; for example, when loading into a table. |
|  | `bytes_written_to_result` | DOUBLE | Bytes written to a result object.  For example, `SELECT * FROM ...` would produce a set of results in tabular format representing each field in the selection.  In general, the results object represents whatever is produced as a result of the query, and `bytes_written_to_result` represents the size of the returned result. |
|  | `bytes_read_from_result` | DOUBLE | Bytes read from a result object. |
|  | `external_bytes_scanned` | DOUBLE | Bytes read from an external object; for example, a stage. |
| `network` | `network_bytes` | DOUBLE | Amount of data sent over the network. |
| `output_rows` |  | INTEGER | Number of output rows. This can be missing for the operator that returns the results to the user; which is usually the RESULT operator. |
| `pruning` |  |  | Information on table pruning. |
|  | `partitions_pruned_by_snowflake_optima` | DOUBLE | Number of partitions pruned by Snowflake Optima. |
|  | `partitions_scanned` | DOUBLE | Number of partitions scanned so far. |
|  | `partitions_total` | DOUBLE | Total number of partitions in a given table. |
| `spilling` |  |  | Information about disk usage for operations in which intermediate results do not fit in memory. |
|  | `bytes_spilled_remote_storage` | DOUBLE | Volume of data spilled to remote disk. |
|  | `bytes_spilled_local_storage` | DOUBLE | Volume of data spilled to local disk. |
| `search_optimization` |  |  | Information about queries that use the [search optimization service](/user-guide/search-optimization-service). |
|  | `partitions_pruned_by_search_optimization` | DOUBLE | Number of partitions pruned by search optimization. |
|  | `partitions_pruned_by_search_optimization_and_snowflake_optima` | DOUBLE | Number of partitions pruned by search optimization and Snowflake Optima. |

Expand

Show lessSee more

### EXECUTION\_TIME\_BREAKDOWN

The fields in the OBJECTs for the `EXECUTION_TIME_BREAKDOWN` column are shown below.

| Key | Data type | Description |
| --- | --- | --- |
| `overall_percentage` | DOUBLE | Percentage of the total query time spent by this operator. |
| `initialization` | DOUBLE | Time spent setting up query processing. |
| `processing` | DOUBLE | Time spent processing the data by the CPU. |
| `synchronization` | DOUBLE | Time spent synchronizing activities between participating processes. |
| `local_disk_io` | DOUBLE | Time during which processing was blocked while waiting for local disk access. |
| `remote_disk_io` | DOUBLE | Time during which processing was blocked while waiting for remote disk access. |
| `network_communication` | DOUBLE | Time during which processing was waiting for network data transfer. |

Expand

Show lessSee more

### OPERATOR\_ATTRIBUTES

Each output row describes one operator in the query.
The following table shows the possible types of operators; for example, the Filter operator.
For each type of operator, the table shows the possible attributes; for example, the expression used to filter the rows.

The operator attributes are stored in the `OPERATOR_ATTRIBUTES` column, which is of type VARIANT and contains an
[OBJECT](/sql-reference/data-types-semistructured#label-data-type-object). The OBJECT contains key/value pairs. Each key corresponds to one attribute of the operator.

| Operator name | Key | Data type | Description |
| --- | --- | --- | --- |
| `Aggregate` |  |  |  |
|  | `functions` | ARRAY of VARCHAR | List of functions computed. |
|  | `grouping_keys` | ARRAY of VARCHAR | Group-by expression. |
| `CartesianJoin` |  |  |  |
|  | `additional_join_condition` | VARCHAR | Non-equality join expression. |
|  | `equality_join_condition` | VARCHAR | Equality join expression. |
|  | `join_type` | VARCHAR | Type of join (INNER). |
| `Delete` | `table_name` | VARCHAR | Name of updated table. |
| `ExternalScan` |  |  |  |
|  | `stage_name` | VARCHAR | The name of the stage from which the data is read. |
|  | `stage_type` | VARCHAR | The type of the stage. |
| `Filter` | `filter_condition` | VARCHAR | The expression used to filter data. |
| `Flatten` | `input` | VARCHAR | Input expression used to flatten data. |
| `Generator` |  |  |  |
|  | `row_count` | NUMBER | Value of the input parameter ROWCOUNT. |
|  | `time_limit` | NUMBER | Value of the input parameter TIMELIMIT. |
| `GroupingSets` |  |  |  |
|  | `functions` | ARRAY of VARCHAR | List of functions computed. |
|  | `key_sets` | ARRAY of VARCHAR | List of grouping sets. |
| `Insert` |  |  |  |
|  | `input_expression` | VARCHAR | Which expressions are inserted. |
|  | `table_names` | ARRAY of VARCHAR | List of table names to which records are added. |
| `InternalObject` | `object_name` | VARCHAR | Name of the accessed object. |
| `Join` |  |  |  |
|  | `additional_join_condition` | VARCHAR | Non-equality join expression. |
|  | `equality_join_condition` | VARCHAR | Equality join expression. |
|  | `join_type` | VARCHAR | Type of join (INNER, OUTER, LEFT JOIN, etc.). |
| `JoinFilter` | `join_id` | NUMBER | Operator id of the join used to identify tuples that can be filtered out. |
| `Merge` | `table_name` | VARCHAR | Name of updated table. |
| `Pivot` |  |  |  |
|  | `grouping_keys` | ARRAY of VARCHAR | Remaining columns on which the results are aggregated. |
|  | `pivot_column` | ARRAY of VARCHAR | Resulting columns of pivot values. |
| `Result` | `expressions` | ARRAY of VARCHAR | List of expressions produced. |
| `Sort` | `sort_keys` | ARRAY of VARCHAR | Expression defining the sorting order. |
| `SortWithLimit` |  |  |  |
|  | `offset` | NUMBER | Position in the ordered sequence from which produced tuples are emitted. |
|  | `rows` | NUMBER | Number of rows produced. |
|  | `sort_keys` | ARRAY of VARCHAR | Expression defining the sorting order. |
| `TableScan` |  |  |  |
|  | `columns` | ARRAY of VARCHAR | List of scanned columns. |
|  | `extracted_variant_paths` | ARRAY of VARCHAR | List of paths extracted from variant columns. |
|  | `table_alias` | VARCHAR | Alias of table being accessed. |
|  | `table_name` | VARCHAR | Name of table being accessed. |
| `Unload` | `location` | VARCHAR | Stage where data is saved. |
| `Unpivot` | `expressions` | ARRAY of VARCHAR | Output columns of the unpivot query. |
| `Update` | `table_name` | VARCHAR | Name of updated table. |
| `ValuesClause` |  |  |  |
|  | `value_count` | NUMBER | Number of produced values. |
|  | `values` | VARCHAR | List of values. |
| `WindowFunction` | `functions` | ARRAY of VARCHAR | List of functions computed. |
| `WithClause` | `name` | VARCHAR | Alias of WITH clause. |

Expand

Show lessSee more

If an operator is not listed, no attributes are produced, and the value is reported as `{}`.

Note

- The following operators do not have any operator attributes and therefore are not included in the
  [table](#label-get-query-operator-stats-operator-attributes) of `OPERATOR_ATTRIBUTES`:
  - `UnionAll`
  - `ExternalFunction`

## Examples

The following examples call the GET\_QUERY\_OPERATOR\_STATS function.

### Retrieving data about a single query

This example shows the statistics for a SELECT that joins two small tables.

Run the SELECT statement:

Copy code

```
SELECT x1.i, x2.i
  FROM x1 INNER JOIN x2 ON x2.i = x1.i
  ORDER BY x1.i, x2.i;
```

Get the query ID:

Copy code

```
SET lqid = (SELECT LAST_QUERY_ID());
```

Call GET\_QUERY\_OPERATOR\_STATS() to get statistics about the individual query operators in the query:

Copy code

```
SELECT * FROM TABLE(GET_QUERY_OPERATOR_STATS($lqid));
```

```
+--------------------------------------+---------+-------------+--------------------+---------------+-----------------------------------------+-----------------------------------------------+----------------------------------------------------------------------+
| QUERY_ID                             | STEP_ID | OPERATOR_ID | PARENT_OPERATORS   | OPERATOR_TYPE | OPERATOR_STATISTICS                     | EXECUTION_TIME_BREAKDOWN                      | OPERATOR_ATTRIBUTES                                                  |
|--------------------------------------+---------+-------------+--------------------+---------------+-----------------------------------------+-----------------------------------------------+----------------------------------------------------------------------|
| 01a8f330-0507-3f5b-0000-43830248e09a |       1 |           0 |               NULL | Result        | {                                       | {                                             | {                                                                    |
|                                      |         |             |                    |               |   "input_rows": 64                      |   "overall_percentage": 0.000000000000000e+00 |   "expressions": [                                                   |
|                                      |         |             |                    |               | }                                       | }                                             |     "X1.I",                                                          |
|                                      |         |             |                    |               |                                         |                                               |     "X2.I"                                                           |
|                                      |         |             |                    |               |                                         |                                               |   ]                                                                  |
|                                      |         |             |                    |               |                                         |                                               | }                                                                    |
| 01a8f330-0507-3f5b-0000-43830248e09a |       1 |           1 |              [ 0 ] | Sort          | {                                       | {                                             | {                                                                    |
|                                      |         |             |                    |               |   "input_rows": 64,                     |   "overall_percentage": 0.000000000000000e+00 |   "sort_keys": [                                                     |
|                                      |         |             |                    |               |   "output_rows": 64                     | }                                             |     "X1.I ASC NULLS LAST",                                           |
|                                      |         |             |                    |               | }                                       |                                               |     "X2.I ASC NULLS LAST"                                            |
|                                      |         |             |                    |               |                                         |                                               |   ]                                                                  |
|                                      |         |             |                    |               |                                         |                                               | }                                                                    |
| 01a8f330-0507-3f5b-0000-43830248e09a |       1 |           2 |              [ 1 ] | Join          | {                                       | {                                             | {                                                                    |
|                                      |         |             |                    |               |   "input_rows": 128,                    |   "overall_percentage": 0.000000000000000e+00 |   "equality_join_condition": "(X2.I = X1.I)",                        |
|                                      |         |             |                    |               |   "output_rows": 64                     | }                                             |   "join_type": "INNER"                                               |
|                                      |         |             |                    |               | }                                       |                                               | }                                                                    |
| 01a8f330-0507-3f5b-0000-43830248e09a |       1 |           3 |              [ 2 ] | TableScan     | {                                       | {                                             | {                                                                    |
|                                      |         |             |                    |               |   "io": {                               |   "overall_percentage": 0.000000000000000e+00 |   "columns": [                                                       |
|                                      |         |             |                    |               |     "bytes_scanned": 1024,              | }                                             |     "I"                                                              |
|                                      |         |             |                    |               |     "percentage_scanned_from_cache": 1, |                                               |   ],                                                                 |
|                                      |         |             |                    |               |     "scan_progress": 1                  |                                               |   "table_name": "MY_DB.MY_SCHEMA.X2" |
|                                      |         |             |                    |               |   },                                    |                                               | }                                                                    |
|                                      |         |             |                    |               |   "output_rows": 64,                    |                                               |                                                                      |
|                                      |         |             |                    |               |   "pruning": {                          |                                               |                                                                      |
|                                      |         |             |                    |               |     "partitions_scanned": 1,            |                                               |                                                                      |
|                                      |         |             |                    |               |     "partitions_total": 1               |                                               |                                                                      |
|                                      |         |             |                    |               |   }                                     |                                               |                                                                      |
|                                      |         |             |                    |               | }                                       |                                               |                                                                      |
| 01a8f330-0507-3f5b-0000-43830248e09a |       1 |           4 |              [ 2 ] | JoinFilter    | {                                       | {                                             | {                                                                    |
|                                      |         |             |                    |               |   "input_rows": 64,                     |   "overall_percentage": 0.000000000000000e+00 |   "join_id": "2"                                                     |
|                                      |         |             |                    |               |   "output_rows": 64                     | }                                             | }                                                                    |
|                                      |         |             |                    |               | }                                       |                                               |                                                                      |
| 01a8f330-0507-3f5b-0000-43830248e09a |       1 |           5 |              [ 4 ] | TableScan     | {                                       | {                                             | {                                                                    |
|                                      |         |             |                    |               |   "io": {                               |   "overall_percentage": 0.000000000000000e+00 |   "columns": [                                                       |
|                                      |         |             |                    |               |     "bytes_scanned": 1024,              | }                                             |     "I"                                                              |
|                                      |         |             |                    |               |     "percentage_scanned_from_cache": 1, |                                               |   ],                                                                 |
|                                      |         |             |                    |               |     "scan_progress": 1                  |                                               |   "table_name": "MY_DB.MY_SCHEMA.X1" |
|                                      |         |             |                    |               |   },                                    |                                               | }                                                                    |
|                                      |         |             |                    |               |   "output_rows": 64,                    |                                               |                                                                      |
|                                      |         |             |                    |               |   "pruning": {                          |                                               |                                                                      |
|                                      |         |             |                    |               |     "partitions_scanned": 1,            |                                               |                                                                      |
|                                      |         |             |                    |               |     "partitions_total": 1               |                                               |                                                                      |
|                                      |         |             |                    |               |   }                                     |                                               |                                                                      |
|                                      |         |             |                    |               | }                                       |                                               |                                                                      |
+--------------------------------------+---------+-------------+--------------------+---------------+-----------------------------------------+-----------------------------------------------+----------------------------------------------------------------------+
```

### Identifying “exploding” join operators

The following example shows how to use GET\_QUERY\_OPERATOR\_STATS to examine a complicated query. This example looks for operators
within a query that produce many more rows than were input to that operator.

This is the query to be analyzed:

Copy code

```
SELECT *
  FROM t1
    JOIN t2 ON t1.a = t2.a
    JOIN t3 ON t1.b = t3.b
    JOIN t4 ON t1.c = t4.c;
```

Get the query ID of the previous query:

Copy code

```
SET lid = LAST_QUERY_ID();
```

The following query shows the ratio of output rows to input rows for each of the join operators in the query:

Copy code

```
SELECT  operator_id,
        operator_attributes,
        operator_statistics:output_rows / operator_statistics:input_rows AS row_multiple
  FROM TABLE(GET_QUERY_OPERATOR_STATS($lid))
  WHERE operator_type = 'Join'
  ORDER BY step_id, operator_id;
```

```
+---------+-------------+--------------------------------------------------------------------------+---------------+
| STEP_ID | OPERATOR_ID | OPERATOR_ATTRIBUTES                                                      | ROW_MULTIPLE  |
+---------+-------------+--------------------------------------------------------------------------+---------------+
|       1 |           1 | {  "equality_join_condition": "(T4.C = T1.C)",   "join_type": "INNER"  } |  49.969249692 |
|       1 |           3 | {  "equality_join_condition": "(T3.B = T1.B)",   "join_type": "INNER"  } | 116.071428571 |
|       1 |           5 | {  "equality_join_condition": "(T2.A = T1.A)",   "join_type": "INNER"  } |  12.20657277  |
+---------+-------------+--------------------------------------------------------------------------+---------------+
```

After you identify the exploding joins, you can review each join condition to verify that the condition is correct.
