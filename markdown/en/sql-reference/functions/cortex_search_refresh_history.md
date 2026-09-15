Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# CORTEX\_SEARCH\_REFRESH\_HISTORY

This table function returns information about each refresh (completed and running) of [Cortex Search services](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview).

This table function returns all refreshes that are in progress as well as all refreshes that have a DATA\_TIMESTAMP within 7 days
of the current time.

## Syntax

Copy code

```
CORTEX_SEARCH_REFRESH_HISTORY(
  [ NAME => '<string>' ]
  [ , DATA_TIMESTAMP_START => <constant_expr> ]
  [ , DATA_TIMESTAMP_END => <constant_expr> ]
  [ , RESULT_LIMIT => <integer> ]
)
```

## Arguments

All the arguments are optional.
If no arguments are provided, 100 refreshes from all Cortex Search services in the account will be returned.

`NAME => string`
:   The name of a Cortex Search service.

    Names must be single-quoted and are case insensitive.

    You can specify the unqualified name (`service_name`),
    the partially qualified name (`schema_name.service_name`),
    or the fully qualified name (`database_name.schema_name.service_name`).

    For more information on object name resolution, refer to [Object name resolution](/sql-reference/name-resolution).

    The function returns the refreshes for this service.

`DATA_TIMESTAMP_START => constant_expr` , `DATA_TIMESTAMP_END => constant_expr`
:   Time range (in TIMESTAMP\_LTZ format) during which the refreshes occurred.

    - If neither a start time nor an end time is specified, the default range will be the past day.
    - If an end time is not specified, [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp) is used as the end of the range.
    - If a start time is not specified, the range starts 1 day prior to the start of DATA\_TIMESTAMP\_END.

`RESULT_LIMIT => integer`
:   A number specifying the maximum number of rows returned by the function. If the number of matching rows is greater than
    this limit, the refreshes that finished most recently (and those that are still running) are returned, up to the specified
    limit.

    To apply a filter on the results, also specify a large enough RESULT\_LIMIT limit value for the filter to be applied on all
    Cortex Search services.

    Range: `1` to `10000`

    Default: `100`.

## Output

The function returns the following columns.

| Column Name | Data Type | Description |
| --- | --- | --- |
| NAME | TEXT | Name of the Cortex Search service. |
| SCHEMA\_NAME | TEXT | Name of the schema that contains the Cortex Search service. |
| DATABASE\_NAME | TEXT | Name of the database that contains the Cortex Search service. |
| STATE | TEXT | Status of the refresh for the Cortex Search service. The status can be one of the following:   - EXECUTING: refresh in progress. - SUCCEEDED: refresh completed successfully. - FAILED: refresh failed during execution. - CANCELLED: refresh was canceled before execution. |
| DATA\_TIMESTAMP | TIMESTAMP\_LTZ | Transactional timestamp when the refresh was evaluated. (This might be slightly before the actual time of the refresh.) All data, in base objects, that arrived before this timestamp is currently included in the Cortex Search service. |
| REFRESH\_START\_TIME | TIMESTAMP\_LTZ | Time when the refresh job started. |
| REFRESH\_END\_TIME | TIMESTAMP\_LTZ | Time when the refresh completed. |
| INDEX\_PREPROCESSING\_DURATION | NUMBER | Duration of the index preprocessing phase in milliseconds. |
| INDEX\_PREPROCESSING\_QUERY\_ID | TEXT | ID of the query that performed the index preprocessing. |
| INDEX\_PREPROCESSING\_STATISTICS | OBJECT | Contains the following properties for index preprocessing:   - `compilationTimeMs`: Time spent compiling the query in milliseconds. - `executionTimeMs`: Time spent executing the query in milliseconds. - `queuedTimeMs`: Time spent queued before execution in milliseconds. - `numInsertedRows`: The number of inserted rows. - `numDeletedRows`: The number of rows that were deleted. - `numCopiedRows`: The number of rows that were copied unchanged. - `numAddedPartitions`: The number of added partitions. - `numRemovedPartitions`: The number of removed partitions. |
| INDEXING\_DURATION | NUMBER | Duration of the indexing phase in milliseconds. |
| INDEXING\_QUERY\_ID | TEXT | ID of the query that performed the indexing. |
| REFRESH\_ACTION | TEXT | One of:   - NO\_DATA - no new data in base tables. - FULL - full refresh of the Cortex Search service. - INCREMENTAL - incremental refresh of the Cortex Search service. |
| REFRESH\_TRIGGER | TEXT | One of:   - SCHEDULED - normal background refresh to keep the service up to date. - MANUAL - user manually triggered refresh using ALTER CORTEX SEARCH SERVICE. - CREATION - refresh performed during the creation DDL statement. |
| TARGET\_LAG\_SEC | NUMBER | Describes the target lag value for the Cortex Search service at the time the refresh occurred. |
| WAREHOUSE | TEXT | Name of the warehouse used for the refresh operation. |
| ERROR | TEXT | Error message if the refresh failed, otherwise NULL. |

Expand

Show lessSee more

## Usage notes

- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Find failed Cortex Search service refreshes during the past week:

Copy code

```
SELECT
  data_timestamp,
  database_name,
  schema_name,
  name,
  state,
  error,
  refresh_trigger
FROM
  TABLE (
    INFORMATION_SCHEMA.CORTEX_SEARCH_REFRESH_HISTORY (
      DATA_TIMESTAMP_START => DATEADD(WEEK, -1, CURRENT_TIMESTAMP())
    )
  )
ORDER BY
  data_timestamp DESC
LIMIT 10;
```

Find recent manual refreshes for a specific Cortex Search service:

Copy code

```
SELECT
  data_timestamp,
  refresh_start_time,
  refresh_end_time,
  refresh_action,
  state
FROM
  TABLE (
    INFORMATION_SCHEMA.CORTEX_SEARCH_REFRESH_HISTORY (
      NAME => 'MYSVC',
      DATA_TIMESTAMP_START => DATEADD(DAY, -7, CURRENT_TIMESTAMP()),
      RESULT_LIMIT => 20
    )
  )
WHERE
  refresh_trigger = 'MANUAL'
ORDER BY
  data_timestamp DESC;
```

Analyze refresh performance for a Cortex Search service:

Copy code

```
SELECT
  name,
  data_timestamp,
  index_preprocessing_duration,
  indexing_duration,
  TIMEDIFF(SECOND, refresh_start_time, refresh_end_time) AS total_refresh_duration_sec,
  index_preprocessing_statistics:numInsertedRows AS rows_processed
FROM
  TABLE (
    INFORMATION_SCHEMA.CORTEX_SEARCH_REFRESH_HISTORY (
      NAME => 'MYSVC',
      DATA_TIMESTAMP_START => DATEADD(DAY, -30, CURRENT_TIMESTAMP())
    )
  )
WHERE
  state = 'SUCCEEDED'
ORDER BY
  data_timestamp DESC;
```
