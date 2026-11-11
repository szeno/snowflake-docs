Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$LOCATE\_DBT\_ARTIFACTS

Returns the location of artifacts from a specified dbt project object run (for example, `manifest.json`).

Use this function with the [DBT\_PROJECT\_EXECUTION\_HISTORY](/sql-reference/functions/dbt_project_execution_history) function to access dbt artifacts and logs programmatically.

## Syntax

Copy code

```
SYSTEM$LOCATE_DBT_ARTIFACTS ( '<query_id>' )
```

## Arguments

`query_id`
:   The query ID of the dbt project object run whose files you want to locate.

## Returns

The function returns the file path for dbt project object artifacts from a run (for example, `snow://dbt/DBTEST.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf3f5a-010b-4d87-0000-53493abb7cce/`).

For more information and examples, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).

This is the results directory for the specified query, not a search for the latest execution. Its standalone target files can include
`manifest.json`, `semantic_manifest.json`, `run_results.json`, and `sources.json` when present, and `logs/dbt.log` contains the current
execution’s log. For the complete directory layout, see
[Results directory contents](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-results-directory-contents).

The function returns a location. Use `LIST` to inspect the returned location or `GET` to download files. When used in the `IMPORTS` clause
of [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project), `SYSTEM$LOCATE_DBT_ARTIFACTS` imports the results directory, including
`dbt_artifacts.zip`, but doesn’t extract the ZIP file. When you import the location `AS 'state'`, Snowflake mounts the query’s results
directory at `./imports/state`, with the dbt artifacts in `./imports/state/target`. Use `SYSTEM$LOCATE_DBT_ARCHIVE` directly when you need
the archived target and logs, such as compiled SQL. Snowflake extracts the archive automatically.

## Access control requirements

This function can only be used with dbt project objects, not Workspaces, when you have one of the following privileges:

- OWNERSHIP, USAGE, or MONITOR on the dbt project object

For details about these privileges, see [dbt project object privileges](/user-guide/security-access-control-privileges#label-access-control-privs-dbt).

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- This system function works only on dbt project objects and isn’t available for Workspaces.
- Query IDs generated from CREATE DBT PROJECT or ALTER DBT PROJECT … DEPLOY aren’t supported for this system function.
- Direct querying of file content (for example, [Query examples](/user-guide/querying-stage#label-querying-stage-query-examples)) isn’t supported.
- If `query_id` is NULL or not a dbt execution, you’ll get an error.
- dbt project results are available for up to 14 days.
- Files might be unavailable if a run times out, is canceled, or fails before they are uploaded. In such cases, runs appear as `UNHANDLED ERROR` in dbt history.
- You can’t use this function to locate artifacts for runs that are in progress because artifacts are only available after the run is complete.

## Examples

To view the stage path where Snowflake stored the dbt project object execution artifacts, use the SYSTEM$LOCATE\_DBT\_ARTIFACTS function, as shown in the following
example. You can then use that path with `GET` or `COPY FILES` or the Snowflake CLI to download files such as `manifest.json` and the run logs. Compiled SQL files are only available inside the `dbt_artifacts.zip` archive, not as separate files in the folder.

Tip

Use function arguments such as `DATABASE`, `SCHEMA`, and `OBJECT_NAME` to filter results whenever possible. These filters are applied before the `RESULT_LIMIT` (default: 100 rows), so using them ensures you get the most relevant results rather than filtering a potentially truncated result set with a `WHERE` clause.

Copy code

```
--Look up the most recent dbt project object execution
SET latest_query_id = (SELECT query_id
  FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.DBT_PROJECT_EXECUTION_HISTORY(
    DATABASE => 'ANALYTICS_DB',
    SCHEMA => 'DBT_PROD',
    OBJECT_NAME => 'FINANCE_ANALYTICS'
  ))
  ORDER BY query_end_time DESC LIMIT 1);

--Get the location of the dbt project object artifacts folder
SELECT SYSTEM$LOCATE_DBT_ARTIFACTS($latest_query_id);
```

```
+-------------------------------------------------------------------------------------------------+
| SYSTEM$LOCATE_DBT_ARTIFACTS($LATEST_QUERY_ID)                                                   |
+-------------------------------------------------------------------------------------------------+
| snow://dbt/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01c01096-010c-0ccb-0000-a99506bd199e/ |
+-------------------------------------------------------------------------------------------------+
```

Copy code

```
--List all the files of the retrieved dbt run
ls 'snow://dbt/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf3f5a-010b-4d87-0000-53493abb7cce/';
```

You can also create an internal stage and copy the located artifacts into it for retrieval. For the full example, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).

### Rerun failed models from a specific execution

To rerun only the resources that failed in a specific execution, first look up the query ID of the failed execution. Filter
[`DBT_PROJECT_EXECUTION_HISTORY`](/sql-reference/functions/dbt_project_execution_history) by the dbt project object and by `state = 'HANDLED_ERROR'`. Executions with an `UNHANDLED_ERROR` state might not
have uploaded artifacts.

Copy code

```
SELECT query_id, command, args, query_end_time
  FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.DBT_PROJECT_EXECUTION_HISTORY(
    DATABASE => 'ANALYTICS_DB',
    SCHEMA => 'DBT_PROD',
    OBJECT_NAME => 'FINANCE_ANALYTICS'
  ))
  WHERE state = 'HANDLED_ERROR'
  ORDER BY query_end_time DESC
  LIMIT 5;
```

```
+--------------------------------------+---------+--------------------+----------------------------------+
| QUERY_ID                             | COMMAND | ARGS               | QUERY_END_TIME                   |
|--------------------------------------+---------+--------------------+----------------------------------|
| 01c6a772-001e-db19-0000-5349650b6cfe | run     | --select tag:daily | 2026-11-09 19:16:10.212000+00:00 |
+--------------------------------------+---------+--------------------+----------------------------------+
```

Then pass the query ID to `SYSTEM$LOCATE_DBT_ARTIFACTS` in the `IMPORTS` parameter of [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project).

Importing this location mounts the execution’s entire results directory, and the dbt artifacts are in its `target` subdirectory. When you
import the results `AS 'state'`, set `--state ./imports/state/target`.

The `SYSTEM$DBT_GET_LAST_*_RUN_TARGET` functions work differently. They import `target` directly, so `./imports/state` contains the artifacts you need.

The `result:error+` selector reruns the resources that errored and their downstream dependencies:

Copy code

```
EXECUTE DBT PROJECT analytics_db.dbt_prod.finance_analytics
  ARGS = 'run --state ./imports/state/target --select result:error+'
  IMPORTS = (
    SYSTEM$LOCATE_DBT_ARTIFACTS('01c6a772-001e-db19-0000-5349650b6cfe') AS 'state'
  );
```

In Snowsight, open the failed query in **Query History**, then select **Re-run** in the **dbt Output** section and select **From query ID** to execute a
statement that reruns the models that errored and their downstream dependencies.

To rerun failed resources from the most recent failed execution without looking up a query ID, use
[SYSTEM$DBT\_GET\_LAST\_FAILED\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_failed_run_target).
