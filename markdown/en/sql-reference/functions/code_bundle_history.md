Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# CODE\_BUNDLE\_HISTORY

Returns the run history of [Code Bundles](/developer-guide/code-bundles/code-bundles): one row per run of
[EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle) or [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project),
including anonymous runs (`EXECUTE CODE BUNDLE FROM ...`) and runs submitted through the REST API. All arguments are optional and act as
filters. With no arguments, the function returns the most recent runs, up to `RESULT_LIMIT`.

Use this function to check whether a run succeeded, find a run by its query ID or execution name, and review failures.

See also:
:   [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle), [SHOW CODE BUNDLES](/sql-reference/sql/show-code-bundles),
    [Monitor Code Bundle runs](/developer-guide/code-bundles/code-bundles#monitor-runs)

## Syntax

Copy code

```
CODE_BUNDLE_HISTORY(
  [ BUNDLE_NAME => '<string>' ]
  [ , DATABASE => '<string>' ]
  [ , SCHEMA => '<string>' ]
  [ , ENTRYPOINT => '<string>' ]
  [ , START_TIME_RANGE_START => <constant_expr> ]
  [ , START_TIME_RANGE_END => <constant_expr> ]
  [ , BUNDLE_TYPES => '<string>' ]
  [ , COMPUTE_TYPES => '<string>' ]
  [ , LANGUAGE_TYPES => '<string>' ]
  [ , STATUS => '<string>' ]
  [ , EXECUTION_NAME => '<string>' ]
  [ , QUERY_ID => '<string>' ]
  [ , RESULT_LIMIT => <integer> ]
  [ , PAGE_TOKEN => '<string>' ]
)
```

## Arguments

All arguments are optional.

`BUNDLE_NAME => '<string>'`
:   Name of the Code Bundle to return runs for. You can specify a fully qualified name (`database.schema.bundle`) or a bare name combined with
    `DATABASE` and `SCHEMA`.

`DATABASE => '<string>'`
:   Database used to resolve a bare `BUNDLE_NAME`, or to return runs of Code Bundles in that database. Ignored when `BUNDLE_NAME` is fully
    qualified.

`SCHEMA => '<string>'`
:   Schema used to resolve a bare `BUNDLE_NAME`, or to return runs of Code Bundles in that schema. Ignored when `BUNDLE_NAME` is fully
    qualified.

`ENTRYPOINT => '<string>'`
:   Returns only runs whose entrypoint matches this value exactly (for example, `main.py`, `main.py:run`, or `com.example.MyApp`).

`START_TIME_RANGE_START => <constant_expr>`, `START_TIME_RANGE_END => <constant_expr>`
:   `TIMESTAMP_LTZ` values that bound the start time of the returned runs. Both ends are inclusive.

`BUNDLE_TYPES => '<string>'`
:   Comma-separated, case-insensitive list of bundle types to include: `custom`, `spark`, and `ml`.

`COMPUTE_TYPES => '<string>'`
:   Comma-separated, case-insensitive list of compute types to include: `warehouse` and `compute_pool`.

`LANGUAGE_TYPES => '<string>'`
:   Comma-separated, case-insensitive list of languages to include: `python`, `java`, and `scala`.

`STATUS => '<string>'`
:   A single status to filter by: `pending`, `running`, `done` (or `succeeded`), `failed`, `cancelled` (or `canceled`), or `deleted`.

    These filter values aren’t the same as the values in the `STATUS` column. For example, a successful run has `STATUS` `DONE`.

`EXECUTION_NAME => '<string>'`
:   Returns only runs whose `EXECUTION_NAME`, set with [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle), matches this value
    exactly.

`QUERY_ID => '<string>'`
:   Returns the run started by the statement with this query ID. The query ID of an `EXECUTE CODE BUNDLE` statement identifies its run. It’s the
    same value as the `job_id` returned by a REST submission.

`RESULT_LIMIT => <integer>`
:   Maximum number of rows to return. Default: `100`. Values are limited to the range 1 to 1000.

`PAGE_TOKEN => '<string>'`
:   Returns the runs after the row that the token came from. To get the next page of results, pass the `PAGE_TOKEN` value from the last row of
    the previous call, with the same filters.

## Output

The function returns one row per run, with the following columns:

| Column | Description |
| --- | --- |
| `CODE_BUNDLE_NAME` | Name of the Code Bundle. NULL for an anonymous run. |
| `DATABASE_NAME` | Database of the Code Bundle. NULL for an anonymous run. |
| `SCHEMA_NAME` | Schema of the Code Bundle. NULL for an anonymous run. |
| `ENTRYPOINT` | Entrypoint of the run. |
| `STATUS` | State of the run, for example `DONE` or `FAILED`. |
| `RUNTIME_STATUS_DETAILS` | Additional status details from the runtime, if any. |
| `SQL_ERROR_CODE` | Snowflake error code of a failed run. |
| `ERROR_MESSAGE` | Error message of a failed run. |
| `BUNDLE_TYPE` | Bundle type of the run, for example `SPARK`. |
| `COMPUTE_TYPE` | Compute type that the run used: `WAREHOUSE` or `COMPUTE_POOL`. |
| `LANGUAGE_TYPE` | Language of the run, for example `PYTHON` or `SCALA`. |
| `RUNTIME_NAME` | Name of the runtime that ran the code: the warehouse name, or the name of the service on the compute pool. |
| `START_TIME` | Time when the run started. |
| `END_TIME` | Time when the run finished. NULL while the run is in progress. |
| `QUERY_ID` | Query ID of the statement that started the run. |
| `EXECUTION_NAME` | Execution name set for the run, if any. |
| `RUNTIME_VERSION` | Runtime version that the run used, for example the Python version on a warehouse or the Container Runtime version on a compute pool. |
| `TASK_NAME` | Fully qualified name of the task that started the run. NULL if the run wasn’t started by a task. |
| `PAGE_TOKEN` | Continuation token for the next page of results. Pass it as the `PAGE_TOKEN` argument to get the runs after this row. |

Expand

Show lessSee more

## Usage notes

- Call the function as `SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY`, or qualify it with a database that you can access, such as
  `my_db.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY`. If you call it unqualified and your session has no current database, the query fails.
- The runs that you can see depend on your role’s privileges on the Code Bundle and your `IMPERSONATE` privilege on the user who started each
  run. For details, see
  [Run history and result visibility](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule#label-nb-in-ws-schedule-run-visibility).
- An asynchronous run appears in the history after it starts. If a statement fails before the run starts, for example because the
  entrypoint doesn’t exist, the run doesn’t appear in the history; check the statement’s error instead.

## Examples

Return the most recent runs of a Code Bundle:

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(
    BUNDLE_NAME => 'my_db.my_schema.my_bundle'));
```

Check the status of one run by its query ID:

Copy code

```
SELECT STATUS, ERROR_MESSAGE, START_TIME, END_TIME
  FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(
    QUERY_ID => '01c51743-c819-4261-0000-5349586311aa'));
```

Find failed Python runs on warehouses in the last day:

Copy code

```
SELECT CODE_BUNDLE_NAME, ENTRYPOINT, ERROR_MESSAGE, QUERY_ID
  FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(
    START_TIME_RANGE_START => DATEADD('day', -1, CURRENT_TIMESTAMP()),
    COMPUTE_TYPES => 'warehouse',
    LANGUAGE_TYPES => 'python',
    STATUS => 'failed',
    RESULT_LIMIT => 1000));
```

Find anonymous runs by execution name:

Copy code

```
SELECT QUERY_ID, STATUS, START_TIME
  FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(
    EXECUTION_NAME => 'adhoc_backfill'));
```

Get the next page of results by passing the `PAGE_TOKEN` value from the last row of the previous page:

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(
    BUNDLE_NAME => 'my_db.my_schema.my_bundle',
    RESULT_LIMIT => 100,
    PAGE_TOKEN => '<page_token_from_last_row>'));
```
