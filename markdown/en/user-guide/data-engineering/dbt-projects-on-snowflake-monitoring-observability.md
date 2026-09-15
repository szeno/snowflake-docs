# Monitor dbt Projects on Snowflake

This topic explains the ways you can use monitoring features for dbt Projects on Snowflake to inspect dbt project executions (manual or task-scheduled) and how to view logs and artifacts.

| Section | Description |
| --- | --- |
| [Enable monitoring features for dbt project objects](#label-dbt-monitoring-observability-enable) | Capture logging and tracing events for a dbt project object and for any scheduled task that runs it. To enable this feature, you must set logging, tracing, and metrics on the schema where the dbt project object and task are deployed. |
| [Monitor scheduled executions of dbt project objects](#label-dbt-projects-monitoring-tasks) | In Snowsight, in the navigation menu, select **Transformation** » **dbt Projects** to view run history, task graphs, and query details for dbt project objects. When a workspace is connected to a dbt project object that runs according to a task schedule, you can open task-run history and task graphs from within the workspace. |
| [Access dbt artifacts and logs programmatically](#label-dbt-projects-artifacts-and-logs) | Use the DBT\_PROJECT\_EXECUTION\_HISTORY table function and dbt system functions to access dbt artifacts and logs programmatically. |

Expand

Show lessSee more

## Enable monitoring features for dbt project objects

To enable monitoring features for your dbt project object, set LOG\_LEVEL, TRACE\_LEVEL, and METRIC\_LEVEL on the database and schema where your dbt project object is created, as shown in the following SQL example:

Copy code

```
ALTER SCHEMA my_db.my_dbt_project_schema SET LOG_LEVEL = 'INFO';
ALTER SCHEMA my_db.my_dbt_project_schema SET TRACE_LEVEL = 'ALWAYS';
ALTER SCHEMA my_db.my_dbt_project_schema SET METRIC_LEVEL = 'ALL';
```

## Query the event table for dbt project execution events

After you enable monitoring features, Snowflake writes log entries and trace spans for each dbt project object execution to the account’s active event table. You can query the event table while a dbt project object is still executing to observe its progress live, or after a run completes to diagnose failures.

Note

Event table entries can appear with up to a 10-second delay from when the event occurs. If you’re querying during a live execution, recent events might not be visible immediately.

Note

The examples in this section use `SNOWFLAKE.TELEMETRY.EVENTS`, the [default event table](/developer-guide/logging-tracing/event-table-setting-up). If your account or database uses a custom event table, replace the table reference in these queries. To find your active event table, run one of the following:

Copy code

```
SHOW PARAMETERS LIKE 'EVENT_TABLE' IN ACCOUNT;
SHOW PARAMETERS LIKE 'EVENT_TABLE' IN DATABASE my_db;
```

Note

Before running these queries, make sure you have [enabled monitoring features](#label-dbt-monitoring-observability-enable) on the schema where your dbt project object is deployed.

### Monitor a live execution

To query the event table while a dbt project object is still running, start the execution asynchronously so you get the query ID back immediately. Then use that query ID to filter event table results in a separate session.

With Snowflake CLI, use the `--run-async` flag:

Copy code

```
snow dbt execute --run-async MY_DB.MY_SCHEMA.MY_DBT_PROJECT run
```

The command returns immediately with output like:

```
Command submitted. You can check the result with
`snow sql -q "select execution_status from table(information_schema.query_history_by_user())
where query_id in ('01c5a039-c81a-619f-0000-53495cc5c5a2');"`
```

Copy the query ID from the output, then query the event table in a separate worksheet or session.

If you’re working purely in SQL, you can also get the query ID of the most recent execution from the execution history:

Copy code

```
SET latest_query_id = (SELECT query_id
  FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.DBT_PROJECT_EXECUTION_HISTORY(
    DATABASE => 'MY_DB',
    SCHEMA => 'MY_SCHEMA',
    OBJECT_NAME => 'MY_DBT_PROJECT'
  ))
  ORDER BY query_end_time DESC LIMIT 1);
```

Use the query ID to filter the event table and query periodically to see new log entries as the execution progresses.

### Query logs during or after a dbt project execution

The following query returns log entries for a specific dbt project object, ordered by most recent first. You can run this query while the project is executing to monitor progress live:

Copy code

```
SELECT
  TIMESTAMP,
  RESOURCE_ATTRIBUTES:"snow.executable.name"::STRING AS project_name,
  RECORD:"severity_text"::STRING AS severity,
  VALUE::STRING AS message
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE
  RESOURCE_ATTRIBUTES:"snow.executable.type"::STRING = 'DBT_PROJECT'
  AND RESOURCE_ATTRIBUTES:"snow.executable.name"::STRING = 'MY_DBT_PROJECT'
  AND RESOURCE_ATTRIBUTES:"snow.query.id"::STRING = '<query_id>'
  AND SCOPE:"name"::STRING = 'snow.dbt.logger'
ORDER BY TIMESTAMP ASC
LIMIT 500;
```

### Filter logs by severity

To isolate errors or warnings from a dbt project execution:

Copy code

```
SELECT
  TIMESTAMP,
  RESOURCE_ATTRIBUTES:"snow.executable.name"::STRING AS project_name,
  RECORD:"severity_text"::STRING AS severity,
  VALUE::STRING AS message
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE
  RESOURCE_ATTRIBUTES:"snow.executable.type"::STRING = 'DBT_PROJECT'
  AND RESOURCE_ATTRIBUTES:"snow.executable.name"::STRING = 'MY_DBT_PROJECT'
  AND RESOURCE_ATTRIBUTES:"snow.query.id"::STRING = '<query_id>'
  AND SCOPE:"name"::STRING = 'snow.dbt.logger'
  AND RECORD:"severity_text"::STRING IN ('ERROR', 'WARN')
ORDER BY TIMESTAMP ASC
LIMIT 500;
```

### Query trace spans for a specific execution

To view trace spans that show the execution steps and their duration:

Copy code

```
SELECT
  TIMESTAMP,
  RESOURCE_ATTRIBUTES:"snow.executable.name"::STRING AS project_name,
  RECORD:"name"::STRING AS span_name,
  DATEDIFF('millisecond', START_TIMESTAMP, TIMESTAMP) AS duration_ms
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE
  RECORD_TYPE = 'SPAN'
  AND RESOURCE_ATTRIBUTES:"snow.executable.type"::STRING = 'DBT_PROJECT'
  AND RESOURCE_ATTRIBUTES:"snow.executable.name"::STRING = 'MY_DBT_PROJECT'
  AND RESOURCE_ATTRIBUTES:"snow.query.id"::STRING = '<query_id>'
ORDER BY TIMESTAMP ASC
LIMIT 500;
```

### Scope results to a time window

To narrow results to the last hour (useful during or immediately after a run):

Copy code

```
SELECT
  TIMESTAMP,
  RESOURCE_ATTRIBUTES:"snow.executable.name"::STRING AS project_name,
  RECORD:"severity_text"::STRING AS severity,
  VALUE::STRING AS message
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE
  RESOURCE_ATTRIBUTES:"snow.executable.type"::STRING = 'DBT_PROJECT'
  AND RESOURCE_ATTRIBUTES:"snow.executable.name"::STRING = 'MY_DBT_PROJECT'
  AND RESOURCE_ATTRIBUTES:"snow.query.id"::STRING = '<query_id>'
  AND SCOPE:"name"::STRING = 'snow.dbt.logger'
  AND TIMESTAMP > DATEADD('hour', -1, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP ASC
LIMIT 500;
```

### Correlate logs with trace spans

Use `TRACE_ID` to associate log messages with the span they belong to. This helps you understand which execution step produced a specific log entry:

Copy code

```
SELECT
  logs.TIMESTAMP,
  logs.RECORD:"severity_text"::STRING AS severity,
  logs.VALUE::STRING AS message,
  spans.RECORD:"name"::STRING AS span_name
FROM SNOWFLAKE.TELEMETRY.EVENTS AS logs
JOIN SNOWFLAKE.TELEMETRY.EVENTS AS spans
  ON logs.TRACE:trace_id::STRING = spans.TRACE:trace_id::STRING
  AND logs.TRACE:span_id::STRING = spans.TRACE:span_id::STRING
WHERE
  logs.RECORD_TYPE = 'LOG'
  AND spans.RECORD_TYPE = 'SPAN'
  AND logs.RESOURCE_ATTRIBUTES:"snow.executable.type"::STRING = 'DBT_PROJECT'
  AND logs.RESOURCE_ATTRIBUTES:"snow.executable.name"::STRING = 'MY_DBT_PROJECT'
  AND logs.RESOURCE_ATTRIBUTES:"snow.query.id"::STRING = '<query_id>'
  AND logs.SCOPE:"name"::STRING = 'snow.dbt.logger'
  AND logs.TIMESTAMP > DATEADD('hour', -1, CURRENT_TIMESTAMP())
ORDER BY logs.TIMESTAMP ASC
LIMIT 500;
```

## Monitor scheduled executions of dbt project objects

If you execute a deployed dbt project object on a schedule using a task, and the task is in the same schema as the dbt project object, you can view scheduled tasks directly from the workspace by selecting **Connect** and then **View Schedules**.

Note

This feature is only available for workspaces that are connected to a dbt project object.

**To monitor scheduled execution of a dbt project object from a workspace:**

1. From the dbt project menu on the right side of the project pane, under **Scheduled runs**, choose **View schedules**.
2. From the list, select the schedule (task) that you want to inspect, and then choose **View details**.

   The information pane for the task opens, where you can view **Task details**, the task **Graph** (if applicable), and **Run History** of this task. For more information, see [View tasks and task graphs in Snowsight](/user-guide/ui-snowsight-tasks).
3. From the **Run History** for any scheduled dbt project object execution in the list, select the Open query history button on the far right to view query details, the query profile, and the query telemetry for the run. For more information, see [Review details and profile of a specific query](/user-guide/ui-snowsight-activity#label-snowsight-specific-query-details).

## Monitor dbt project objects in Snowsight

To view detailed monitoring information about dbt project object executions, navigate to **Transformations** » **dbt Projects** in Snowsight. You must use a role with the MONITOR privilege to view monitoring information for the dbt project object.
For more information, see [Access control for dbt projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control).

1. In the navigation menu, select **Transformation** » **dbt Projects**. A histogram shows the frequency of dbt project object executions and a list of projects that have run.

   The list of dbt project objects includes columns with the following information. You can filter the list by date range, command, and run status.

   - **PROJECT** - The name of the dbt project object and the number of executions (runs) in the selected time period.
   - **LAST COMMAND** - The dbt command that executed during the last run.
   - **LAST RUN STATUS** - The result of the run: **Succeeded**, **Executing**, or **Failed**.
   - **LAST RUN** - The elapsed time since the last run. To reverse the sort order, select the column header. The most recent run is shown first by default.
   - **PREVIOUS RUNS** - The number of runs in the selected time period by status.
   - **DATABASE** and **SCHEMA** - The database and schema where the dbt project object is saved.
   - **LAST RUN PARAMETERS** - The dbt command-line arguments (ARGS) specified in the EXECUTE DBT PROJECT command for the last dbt project object execution.
2. To inspect individual project runs, select a dbt project object from the list.

   The dbt project object details page in the database object explorer opens for that dbt project object.

   The **Run History** tab is selected by default, with the following information for each job run in the selected time period:

   - **COMMAND** - The dbt command that executed during the last run.
   - **STATUS** - The result of the run: **Succeeded**, **Executing**, or **Failed**.
   - **RUN TIME** - The elapsed time since the last run. To reverse the sort order, select the column header. The most recent run is shown first by default.
   - **PARAMETERS** The dbt command-line arguments (ARGS) specified in the EXECUTE DBT PROJECT command for the last dbt project object execution.
3. To see details for a run, select it from the list.

   The **Query Details** page opens for the EXECUTE DBT PROJECT query that ran. This page includes the following tabs:

   - **Query Details** - Displays the execution status, start time, end time, duration, warehouse size, query ID, and the SQL text of the EXECUTE DBT PROJECT command. Also shows per-model results for the dbt command that ran (for example, `build`), including each model name, time taken, and status.
   - **Query Profile** - Shows the query execution plan and performance statistics.
   - **Query Telemetry** - Shows telemetry data for the execution.
   - **DAG** - Visualizes the models that ran during the execution and their results. For more information, see [View the query history DAG](#label-dbt-query-history-dag).

   For more information, see [Review details and profile of a specific query](/user-guide/ui-snowsight-activity#label-snowsight-specific-query-details).

### View the query history DAG

The **Query Details** for a dbt project object execution includes a **DAG** tab that visualizes what ran during an
execution and the results for each model. This differs from the DAG on the project details page, which serves as a
documentation layer for your project, including models, tests, sources, and their dependencies.

The query history DAG is built from the `manifest.json` and `run_results.json` artifacts produced during an execution. Select a
node in the DAG to open a side panel with details for that specific query, including the query ID and any error messages if the
query failed. The side panel also shows runtime details for the model run, including:

- Start time, end time, and duration for the model run.
- A link to the target object in the database.
- The query ID for the model’s execution.
- Error messages, if the model failed.

The query history DAG supports the same search bar, depth controls, and column-level lineage as the project details DAG: select
**Show columns** on any node to expand its column list, then select a column to highlight all upstream and downstream models
that use it. For full details on DAG interaction, including a description of each DAG node type, see [View and manage dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake-manage).

To view the query history DAG:

1. In the navigation menu, select **Transformations** » **dbt Projects**.
2. From the list of dbt project objects, select a project.
3. On the **Run History** tab, select a run to open the **Query Details** for that execution.
4. Select the **DAG** tab.

Note

If the query history DAG shows “No data available,” the run likely failed before `run_results.json` could be generated.
For more information, see [Limitations for the query history DAG](/user-guide/data-engineering/dbt-projects-on-snowflake-limitations#label-dbt-limitations-query-history-dag).

## Access dbt artifacts and logs programmatically

Use the [DBT\_PROJECT\_EXECUTION\_HISTORY](/sql-reference/functions/dbt_project_execution_history) table function and the following system functions to access dbt artifacts and logs programmatically.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

The system functions in this section retrieve artifacts and logs from `EXECUTE DBT PROJECT` executions. Automatic compilation during
deployment doesn’t create a per-query execution result, so you can’t use these functions to retrieve its artifacts. Snowflake stores
separate per-query result artifacts and an archive for each execution regardless of `DEFAULT_WRITEBACK` or `WRITEBACK`.

Use [`SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET`](/sql-reference/functions/system_dbt_get_last_successful_run_target),
[`SYSTEM$DBT_GET_LAST_FAILED_RUN_TARGET`](/sql-reference/functions/system_dbt_get_last_failed_run_target), or
[`SYSTEM$DBT_GET_LAST_RUN_TARGET`](/sql-reference/functions/system_dbt_get_last_run_target) to retrieve
reusable dbt artifacts from a dbt project object’s recent executions. For example, Slim CI uses `SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET` to
retrieve dbt artifacts from a production object. These functions require `MONITOR` on the referenced dbt project object, and that object must have at least one qualifying execution within the previous 7 days.

For artifacts from a known query, use `SYSTEM$LOCATE_DBT_ARTIFACTS` or `SYSTEM$LOCATE_DBT_ARCHIVE` with its query ID. Use these system functions when
you’re investigating or importing a specific execution’s results.

Note

The Information Schema table function retains data for 7 days. For longer retention (365 days), use the [DBT\_PROJECT\_EXECUTION\_HISTORY view](/sql-reference/account-usage/dbt_project_execution_history) Account Usage view.

| Function | What it returns | Typical use | Notes |
| --- | --- | --- | --- |
| [SYSTEM$GET\_DBT\_LOG](/sql-reference/functions/system_get_dbt_log) | Text log output (the run’s log tail) | Quick debugging in SQL. For example, see errors and warnings without downloading files. | Returns log content; nothing is created or moved. |
| [SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts) | Folder path (for example, `snow://…/results/query_id_…/`) containing artifact files such as `manifest.json` and logs. Compiled SQL files are available only inside `dbt_artifacts.zip`. | Browse or copy specific files with LIST, GET, or COPY FILES. | Just a locator (a URL); you still run GET/COPY FILES to fetch. |
| [SYSTEM$LOCATE\_DBT\_ARCHIVE](/sql-reference/functions/system_locate_dbt_archive) | Single ZIP file URL (for example, `…/dbt_artifacts.zip`). | Handy when you want to download one file (for example, with GET). | Use `GET '<url>' file:///local/dir` to download. |
| [SYSTEM$DBT\_GET\_LAST\_SUCCESSFUL\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_successful_run_target) | dbt artifacts from a recent successful execution of a specified dbt project object. | Import production dbt artifacts for Slim CI. | Requires `MONITOR` on the referenced dbt project object. |
| [SYSTEM$DBT\_GET\_LAST\_FAILED\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_failed_run_target) | dbt artifacts from a recent failed execution of a specified dbt project object. | Recover from a failed execution with result selectors. | Requires `MONITOR` on the referenced dbt project object. |
| [SYSTEM$DBT\_GET\_LAST\_RUN\_TARGET](/sql-reference/functions/system_dbt_get_last_run_target) | dbt artifacts from the most recent completed execution, successful or failed. | Import dbt artifacts from the latest completed execution. | Requires `MONITOR` on the referenced dbt project object. |

Expand

Show lessSee more

### Get logs and download a ZIP file of the latest dbt project query

The following example queries Snowflake’s dbt execution history to show the most recent query ID for the dbt project object. It pulls the log output
for that execution and returns the location of the zipped dbt artifacts for that execution.

The Snowflake CLI example downloads the artifacts ZIP file or specific files (like `manifest.json`) to your local folder using GET.

To download the ZIP file from Snowsight, navigate to **Transformations** » **dbt Projects**, select your project, then select an execution to navigate to **Query Details**,
and select **Download Build Artifacts** under **dbt Output**.

You must use a role with the OWNERSHIP, USAGE, or MONITOR privilege on your dbt project objects.

Tip

Use function arguments such as `DATABASE`, `SCHEMA`, and `OBJECT_NAME` to filter results whenever possible. These filters are applied before the `RESULT_LIMIT` (default: 100 rows), so using them ensures you get the most relevant results rather than filtering a potentially truncated result set with a `WHERE` clause.

SQLSnowflake CLI

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

--Get the dbt run logs for the most recent dbt project object execution
SELECT SYSTEM$GET_DBT_LOG($latest_query_id);
```

```
============================== 15:14:53.100781 | 46d19186-61b8-4442-8339-53c771083f16 ==============================
[0m15:14:53.100781 [info ] [Dummy-1   ]: Running with dbt=1.9.4
...
[0m15:14:58.198545 [debug] [Dummy-1   ]: Command `cli run` succeeded at 15:14:58.198121 after 5.19 seconds
```

To view the stage path where Snowflake stored the dbt project object execution artifacts, use the
SYSTEM$LOCATE\_DBT\_ARTIFACTS function. You can then use that path with `GET` or `COPY FILES` with the Snowflake CLI to download
files such as `manifest.json` and logs. Compiled SQL files are available only inside the `dbt_artifacts.zip` archive.

Copy code

```
--Get the dbt project object execution artifacts directory
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
--List all the files of a dbt run
ls 'snow://dbt/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf3f5a-010b-4d87-0000-53493abb7cce/';
```

You can also create a fresh internal stage, locate the Snowflake-managed path for the specified dbt project object execution’s artifacts, and copy those
artifacts into your stage for retrieval, as shown in the following example:

Copy code

```
CREATE OR REPLACE STAGE my_dbt_stage ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

SELECT SYSTEM$LOCATE_DBT_ARTIFACTS($latest_query_id);
```

```
snow://dbt/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf51c1-010b-5676-0000-53493ae6db02/
```

Copy code

```
COPY FILES INTO @my_dbt_stage/results/ FROM 'snow://dbt/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf51c1-010b-5676-0000-53493ae6db02/';
```

```
results/dbt_artifacts.zip
results/logs/dbt.log
results/target/manifest.json
results/target/semantic_manifest.json
```

Copy code

```
snowsql -q "SELECT query_id
   FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.DBT_PROJECT_EXECUTION_HISTORY(
     DATABASE => 'ANALYTICS_DB',
     SCHEMA => 'DBT_PROD',
     OBJECT_NAME => 'FINANCE_ANALYTICS'
   ))
   ORDER BY query_end_time DESC LIMIT 1;"

snowsql -q "SELECT SYSTEM\$GET_DBT_LOG('01bf3f89-0300-0001-0000-0000000c1229')"
```

```
| ============================== 11:17:39.152234 | 4df65841-7aa3-40e2-81cb-2007c09c2b81
| 11:17:39.152234 [info ] [Dummy-1   ]: Running with dbt=1.9.4
....
```

Copy code

```
snowsql -q "SELECT SYSTEM\$LOCATE_DBT_ARCHIVE('01bf3f89-0300-0001-0000-0000000c1229')"
```

```
snow://dbt_project/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf3f89-0300-0001-0000-0000000c1229/dbt_artifacts.zip
```

Copy code

```
snowsql -q "GET 'snow://dbt_project/TESTDBT.PUBLIC.MY_DBT_PROJECT/results/query_id_01bf3f89-0300-0001-0000-0000000c1229/dbt_artifacts.zip' file:///Users/user_name/Code/temp"
```

```
Type SQL statements or !help
+-----------------------------------------------------------------+--------+------------+-----
| file                                                            |   size | status    | ....
|-----------------------------------------------------------------+--------+------------+-----
| query_id_01bf3f89-0300-0001-0000-0000000c1229/dbt_artifacts.zip | 137351 | DOWNLOADED |...
+-----------------------------------------------------------------+--------+------------+-----
```

Note

The dbt log file (`dbt.log`) is written at `debug` level by default, which produces verbose output including internal dbt
engine details. To capture less verbose output, pass `--log-level-file info` in your EXECUTE DBT PROJECT ARGS. For more
information, see [Supported dbt commands and flags](/user-guide/data-engineering/dbt-projects-on-snowflake-supported-commands).
