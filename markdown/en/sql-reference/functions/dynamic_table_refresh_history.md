Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# DYNAMIC\_TABLE\_REFRESH\_HISTORY

This table function returns information about each refresh (completed and running) of [dynamic tables](/user-guide/dynamic-tables/overview).

This table function returns all refreshes that are in progress as well as all refreshes that have a DATA\_TIMESTAMP within 7 days
of the current time.

## Syntax

Copy code

```
DYNAMIC_TABLE_REFRESH_HISTORY(
  [ DATA_TIMESTAMP_START => <constant_expr> ]
  [ , DATA_TIMESTAMP_END => <constant_expr> ]
  [ , RESULT_LIMIT => <integer> ]
  [ , NAME => '<string>' ]
  [ , NAME_PREFIX => '<string>' ]
  [ , ERROR_ONLY => { TRUE | FALSE } ]
)
```

## Arguments

All the arguments are optional.
If no arguments are provided, 100 refreshes from all dynamic tables in the account will be returned.

`DATA_TIMESTAMP_START => constant_expr` , `DATA_TIMESTAMP_END => constant_expr`
:   Time range (in TIMESTAMP\_LTZ format) during which the refreshes occurred.

    - If neither a start version nor an end version is specified, the default range will be the past day.
    - If an end version is not specified, [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp) is used as the end of the range.
    - If a start version is not specified, the range starts 1 day prior to the start of DATE\_TIMESTAMP\_END.

`RESULT_LIMIT => integer`
:   A number specifying the maximum number of rows returned by the function. If the number of matching rows is greater than
    this limit, the refreshes that finished most recently (and those that are still running) are returned, up to the specified
    limit.

    To apply a filter on the results, also specify a large enough RESULT\_LIMIT limit value for the filter to be applied on all
    dynamic tables.

    Range: `1` to `10000`

    Default: `100`.

`NAME => string`
:   The name of a dynamic table.

    Names must be single-quoted and are case insensitive.

    You can specify the unqualified name (`dynamic_table_name`),
    the partially qualified name (`schema_name.dynamic_table_name`),
    or the fully qualified name (`database_name.schema_name.dynamic_table_name`).

    For more information on object name resolution, refer to [Object name resolution](/sql-reference/name-resolution).

    The function returns the refreshes for this table.

`NAME_PREFIX => string`
:   A prefix for dynamic tables.

    Name prefixes must be single-quoted and are case insensitive.

    The function returns refreshes for tables with names that start with this prefix.

    You can use this argument to return the refreshes for dynamic tables in a specific database or schema.

`ERROR_ONLY => TRUE | FALSE`
:   When set to TRUE, this function returns only refreshes that failed or were cancelled.

## Output

The function returns the following columns.

To view these columns, you must use a role with the MONITOR privilege. For more information, see
[Grant MONITOR to view metadata](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges-view-metadata).

| Column Name | Data Type | Description |
| --- | --- | --- |
| NAME | TEXT | Name of the dynamic table. |
| SCHEMA\_NAME | TEXT | Name of the schema that contains the dynamic table. |
| DATABASE\_NAME | TEXT | Name of the database that contains the dynamic table. |
| STATE | TEXT | Status of the refresh for the dynamic table. The status can be one of the following:   - SCHEDULED: refresh scheduled, but not yet executed. - EXECUTING: refresh in progress. - SUCCEEDED: refresh completed successfully. - FAILED: refresh failed during execution. - CANCELLED: refresh was canceled before execution. - UPSTREAM\_FAILED: refresh not performed due to an upstream failed refresh. - SKIPPED: refresh not performed because an upstream dynamic table refresh was skipped or the scheduler deferred the   refresh to maximize time within target lag. |
| STATE\_CODE | TEXT | Code representing the current state of the refresh. |
| STATE\_MESSAGE | TEXT | Description of the current state of the refresh. |
| QUERY\_ID | TEXT | ID of the SQL statement that produced the results for the dynamic table. |
| DATA\_TIMESTAMP | TIMESTAMP\_LTZ | Transactional timestamp when the refresh was evaluated. (This might be slightly before the actual time of the refresh.) All data, in base objects, that arrived before this timestamp is currently included in the dynamic table. |
| REFRESH\_START\_TIME | TIMESTAMP\_LTZ | Time when the refresh job started. |
| REFRESH\_END\_TIME | TIMESTAMP\_LTZ | Time when the refresh completed. |
| COMPLETION\_TARGET | TIMESTAMP\_LTZ | Time by which this refresh should complete to keep lag under the TARGET\_LAG parameter for the dynamic table. This is equal to the DATA\_TIMESTAMP of the last refresh + TARGET\_LAG. |
| QUALIFIED\_NAME | TEXT | Fully qualified name of the dynamic table as it appears in the graph of dynamic tables. You can use this to join the output with the output of the [DYNAMIC\_TABLE\_GRAPH\_HISTORY](/sql-reference/functions/dynamic_table_graph_history) function. |
| LAST\_COMPLETED\_DEPENDENCY | OBJECT | Contains the following properties:   - `qualified_name`: The qualified name of the latest dependency to become available. - `data_timestamp`: The refresh version of that dependency. |
| STATISTICS | OBJECT | Contains the following properties:   - `numInsertedRows`: The number of inserted rows. - `numDeletedRows`: The number of rows that were deleted. - `numCopiedRows`: The number of rows that were copied unchanged. - `numAddedPartitions`: The number of added partitions. - `numRemovedPartitions` : The number of removed partitions. - `queuedTimeMs`: The time (in milliseconds) spent in the queued state. - `compilationTimeMs`: The time (in milliseconds) spent compiling the refresh query. - `executionTimeMs`: The time (in milliseconds) spent executing the refresh query.   For successful refreshes, this column includes both the row/partition statistics and the time distribution information. For example:  Copy code  ``` {   "numAddedPartitions": 1,   "numCopiedRows": 0,   "numDeletedRows": 25,   "numInsertedRows": 36,   "numRemovedPartitions": 1,   "queuedTimeMs": 123,   "compilationTimeMs": 456,   "executionTimeMs": 789 } ```  For failed refreshes, this column is populated with the time distribution information only. For example:  Copy code  ``` {   "queuedTimeMs": 123,   "compilationTimeMs": 456,   "executionTimeMs": 789 } ```  Note  Because a JSON object is an unordered set of keys and values, the order of properties in the output may vary from the examples above.  For example, if an UPDATE statement updates 1 row in a partition with 10 rows, the row/partition metrics show 1 row inserted, 1 deleted, and 9 copied. Additionally, 1 partition is removed and 1 partition added. |
| REFRESH\_ACTION | TEXT | One of:   - NO\_DATA - no new data in base tables. Doesn’t apply to the initial refresh of newly created dynamic tables regardless of whether or not the base tables have data. - REINITIALIZE - base table changed, source table of a cloned dynamic table was refreshed during clone, or an ADAPTIVE dynamic table chose to reinitialize because processing changes incrementally would be more expensive. - FULL - Full refresh, because dynamic table contains query elements that are not incrementalizable (see SHOW DYNAMIC TABLE refresh\_mode\_reason) or because full refresh was cheaper than incremental refresh. - INCREMENTAL - normal incremental refresh. - CUSTOM\_INCREMENTAL - refresh executed the user-defined DML in the REFRESH USING clause. |
| REINIT\_REASON | TEXT | When REFRESH\_ACTION is REINITIALIZE, describes why the dynamic table was reinitialized, such as base table changes or adaptive refresh mode decisions. NULL for other refresh actions. |
| REFRESH\_TRIGGER | TEXT | One of:   - SCHEDULED - normal background refresh to meet target lag or downstream target lag. - MANUAL - user/task used ALTER DYNAMIC TABLE <name> REFRESH - CREATION - refresh performed during the creation DDL statement, triggered by the creation of the dynamic table or any consumer dynamic tables. |
| TARGET\_LAG\_SEC | NUMBER | Describes the target lag value for the dynamic tables at the time the refresh occurred. |
| GRAPH\_HISTORY\_VALID\_FROM | TIMESTAMP\_NTZ | Encodes the VALID\_FROM timestamp of the DYNAMIC\_TABLE\_GRAPH\_HISTORY table function when the refresh occurred to clarify which version of a dynamic table a specific refresh corresponds to. This value can also be NULL if the corresponding dynamic table hasn’t been created. |
| INPUTS\_WITH\_CHANGED\_DATA | ARRAY of OBJECTs | Each OBJECT represents a table, view, or dynamic table that serves as the input to this dynamic table and had changed data during this refresh. Each OBJECT consists of:   - `name` (TEXT): The fully qualified name. - `kind` (TEXT): The type of input (`TABLE`, `DYNAMIC_TABLE`, or `VIEW`). - `statistics` (OBJECT): Present for `TABLE` and `DYNAMIC_TABLE` inputs. Contains:   - `numRegisteredRows`: The number of rows added to this input.   - `numUnregisteredRows`: The number of rows removed from this input.   - `numAddedPartitions`: The number of added partitions.   - `numRemovedPartitions`: The number of removed partitions. - `baseTableStatisticsAgg` (OBJECT): Present for `VIEW` inputs instead of `statistics`. Contains the same sub-properties. Because views have no DML of their own, this sums the DML statistics from the view’s underlying base tables. If multiple VIEW inputs share an underlying base table, that base table contributes to each view’s statistics independently.   For example:  Copy code  ``` [   {     "name": "MY_DB.MY_SCHEMA.MY_TABLE",     "kind": "TABLE",     "statistics": {       "numRegisteredRows": 9,       "numUnregisteredRows": 0,       "numAddedPartitions": 2,       "numRemovedPartitions": 0     }   },   {     "name": "MY_DB.MY_SCHEMA.MY_VIEW",     "kind": "VIEW",     "baseTableStatisticsAgg": {       "numRegisteredRows": 4,       "numUnregisteredRows": 0,       "numAddedPartitions": 1,       "numRemovedPartitions": 0     }   } ] ```  Note  Because a JSON object is an unordered set of keys and values, the order of properties in the output may vary from the example above.  NULL if:   - REFRESH\_ACTION is NO\_DATA (no input changed). - The refresh failed before it could identify which inputs had changed.   For failed refreshes, the column is populated with any inputs that could be identified as changed before the failure occurred. |

Expand

Show lessSee more

## Usage notes

- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Retrieve the refreshes that failed or were canceled:

> Copy code
>
> ```
> SELECT
>   name,
>   state,
>   state_code,
>   state_message,
>   query_id,
>   data_timestamp,
>   refresh_start_time,
>   refresh_end_time
> FROM
>   TABLE (
>     INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY (
>       NAME_PREFIX => 'MYDB.MYSCHEMA.', ERROR_ONLY => TRUE
>     )
>   )
> ORDER BY
>   name,
>   data_timestamp;
> ```
