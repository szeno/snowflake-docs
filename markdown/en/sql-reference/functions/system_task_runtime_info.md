Categories:
:   [System functions](/sql-reference/functions-system)

# SYSTEM$TASK\_RUNTIME\_INFO

Returns information about the current task run. If this function is called outside of a task run, it fails with an error.

## Syntax

Copy code

```
SYSTEM$TASK_RUNTIME_INFO('<arg_name>')
```

## Arguments

`'arg_name'`
:   Specifies the type of information to return. You can specify one of the following values:

    | Value | Description |
    | --- | --- |
    | `'CURRENT_TASK_NAME'` | Returns the name of the current task. |
    | `'CURRENT_ROOT_TASK_NAME'` | Returns the name of the root task in the current task graph. |
    | `'CURRENT_ROOT_TASK_UUID'` | Returns a universally unique identifier (UUID) that represents the root task in the current task graph. |
    | `'CURRENT_TASK_GRAPH_RUN_GROUP_ID'` | Returns a universally unique identifier (UUID) that represents the current graph run group. |
    | `'CURRENT_TASK_GRAPH_ORIGINAL_SCHEDULED_TIMESTAMP'` | Returns the original scheduled timestamp of the root task in the current graph run group.  For graphs that are retried, the returned value is the original scheduled timestamp of the initial graph run in the current group. |
    | `'LAST_SUCCESSFUL_TASK_GRAPH_RUN_GROUP_ID'` | Returns a universally unique identifier (UUID) that represents the latest successful graph run group.  The value is consistent throughout the graph run group and is determined when the root task of the initial graph run starts. |
    | `'LAST_SUCCESSFUL_TASK_GRAPH_ORIGINAL_SCHEDULED_TIMESTAMP'` | Returns the original scheduled timestamp of the root task in the latest successful graph run group.  The value is consistent throughout the graph run group and is determined when the root task of the initial graph run starts. |

    Expand

    Show lessSee more

## Returns

Returns a STRING or TEXT with requested information.

## Usage notes

- We recommend using SELECT instead of CALL for SYSTEM$TASK\_RUNTIME\_INFO, because SELECT SYSTEM$TASK\_RUNTIME\_INFO automatically converts datatypes, while CALL SYSTEM$TASK\_RUNTIME\_INFO doesn’t.

## Examples

Use CURRENT\_TASK\_GRAPH\_RUN\_GROUP\_ID with CURRENT\_ROOT\_TASK\_NAME for debugging and creating a unique output directory or file:

> Copy code
>
> ```
> CREATE OR REPLACE TASK my_task ...
>   AS
>   ...
>
>   -- Inside Python UDF
>
>   query_result = session.sql("""select
>         SYSTEM$TASK_RUNTIME_INFO('CURRENT_ROOT_TASK_NAME')
>         AS root_name,
>         SYSTEM$TASK_RUNTIME_INFO('CURRENT_TASK_GRAPH_RUN_GROUP_ID')
>         AS run_id""").collect()
>   current_root_task_name, current_graph_run_id = result.ROOT_NAME, result.RUN_ID
>
>   -- Logging information here
>
>   logger.debug(f"start training for {current_root_task_name} at run {current_graph_run_id}")
>
>   -- Create a unique output directory to store intermediate information
>
>   output_dir_name = f"{current_root_task_name}/{current_graph_run_id}/preprocessing.out"
>   with open(output_dir_name, "rw+") as f:
>     ....
> ...;
> ```

Use CURRENT\_TASK\_GRAPH\_ORIGINAL\_SCHEDULED\_TIMESTAMP with LAST\_SUCCESSFUL\_TASK\_GRAPH\_ORIGINAL\_SCHEDULED\_TIMESTAMP to process data from streaming input source:

> Copy code
>
> ```
> CREATE OR REPLACE TASK my_task ...
>   AS
>   ...
>   INSERT INTO my_output_table
>     SELECT * FROM my_source_table
>       WHERE TRUE
>         ...
>         AND TIMESTAMP BETWEEN
>           COALESCE(
>             SYSTEM$TASK_RUNTIME_INFO('LAST_SUCCESSFUL_TASK_GRAPH_ORIGINAL_SCHEDULED_TIMESTAMP')::timestamp_ltz,
>             '2023-07-01'
>           ) AND SYSTEM$TASK_RUNTIME_INFO('CURRENT_TASK_GRAPH_ORIGINAL_SCHEDULED_TIMESTAMP')::timestamp_ltz
>    ...;
> ```

Use LAST\_SUCCESSFUL\_TASK\_GRAPH\_RUN\_GROUP\_ID to generate a unique output directory and log lines:

> Copy code
>
> ```
> CREATE OR REPLACE TASK my_task ...
>   AS
>   ...
>
>   -- Inside Python UDF
>
>   query_result = session.sql("select
>       SYSTEM$TASK_RUNTIME_INFO('CURRENT_ROOT_TASK_NAME') AS root_name, SYSTEM$TASK_RUNTIME_INFO('LAST_SUCCESSFUL_TASK_GRAPH_RUN_GROUP_ID') AS last_run_id").collect()
>   current_root_task_name, last_graph_run_id = query_result.ROOT_NAME,query_result.LAST_RUN_ID
>   logger.log(f"graph name: {current_root_task_name}, last successful run: {last_graph_run_id}")
>   ...;
> ```
