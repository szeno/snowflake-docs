Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DBT\_PROJECT\_EXECUTION\_HISTORY view

This Account Usage view displays the execution history of [dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake). The view retains data for 365 days (1 year).

See also:
:   [DBT\_PROJECT\_EXECUTION\_HISTORY](/sql-reference/functions/dbt_project_execution_history) (Information Schema table function)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| QUERY\_ID | TEXT | ID of the query associated with the execution. |
| QUERY\_START\_TIME | TIMESTAMP\_LTZ | Time the execution started. |
| QUERY\_END\_TIME | TIMESTAMP\_LTZ | Time the execution ended. |
| USER\_ID | TEXT | Internal/system-generated identifier for the user that initiated the execution. Empty for system-initiated runs. |
| USER\_NAME | TEXT | Name of the user that initiated the execution. Displays SYSTEM for system-initiated runs. |
| OBJECT\_NAME | TEXT | Name of the workspace or dbt project object the execution belonged to. |
| OBJECT\_TYPE | TEXT | Type of object. Possible values: - DBT\_PROJECT - WORKSPACE |
| DATABASE\_ID | TEXT | Internal/system-generated identifier for the database containing the object. |
| DATABASE\_NAME | TEXT | Name of the database containing the object. |
| SCHEMA\_ID | TEXT | Internal/system-generated identifier for the schema containing the object. |
| SCHEMA\_NAME | TEXT | Name of the schema containing the object. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse used for the execution. |
| WAREHOUSE\_NAME | TEXT | Name of the warehouse used for the execution. |
| COMMAND | TEXT | The [dbt command](https://docs.getdbt.com/reference/dbt-commands) that was run. |
| ARGS | TEXT | The arguments passed to the dbt command. For example, `--target prod`. |
| ERROR\_CODE | TEXT | Error code for the execution, if applicable. |
| ERROR\_MESSAGE | TEXT | Error message describing why the execution failed, if applicable. |
| STATE | TEXT | State of the execution. Possible values include: - SUCCESS - HANDLED\_ERROR |
| DBT\_VERSION | TEXT | The dbt version used for the execution. For example, `1.10.15`. |
| DBT\_SNOWFLAKE\_VERSION | TEXT | The version of the dbt-snowflake adapter used for the execution. For example, `1.10.3`. |
| ENVIRONMENT | TEXT | The environment (defined in the `env.yml` file) used for this run. For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables). |

Expand

Show lessSee more

## Usage notes

- The latency for this view can be up to 120 minutes (2 hours).
- Data is retained for 365 days (1 year).
- This view includes executions from both dbt project objects and workspaces.
- This view is queried with standard SQL `WHERE` clauses. It doesn’t support the `=>` named-parameter filtering available in the [Information Schema table function](/sql-reference/functions/dbt_project_execution_history). If you only need the last 7 days of history, use the Information Schema table function instead.

## Examples

### Query recent executions for a specific dbt project object

Copy code

```
SELECT
    object_name,
    object_type,
    command,
    args,
    state,
    query_start_time,
    query_end_time,
    user_name
FROM SNOWFLAKE.ACCOUNT_USAGE.DBT_PROJECT_EXECUTION_HISTORY
WHERE database_name = 'ANALYTICS_DB'
  AND schema_name = 'DBT_PROD'
  AND object_name = 'FINANCE_ANALYTICS'
ORDER BY query_start_time DESC
LIMIT 20;
```

### Find failed executions for a specific dbt project object

Copy code

```
SELECT
    object_name,
    database_name,
    schema_name,
    command,
    args,
    error_code,
    error_message,
    query_start_time,
    user_name
FROM SNOWFLAKE.ACCOUNT_USAGE.DBT_PROJECT_EXECUTION_HISTORY
WHERE state != 'SUCCESS'
  AND database_name = 'ANALYTICS_DB'
  AND schema_name = 'DBT_PROD'
ORDER BY query_start_time DESC;
```

### Track dbt version usage across executions

Copy code

```
SELECT
    dbt_version,
    dbt_snowflake_version,
    COUNT(*) AS execution_count,
    MIN(query_start_time) AS first_seen,
    MAX(query_start_time) AS last_seen
FROM SNOWFLAKE.ACCOUNT_USAGE.DBT_PROJECT_EXECUTION_HISTORY
GROUP BY dbt_version, dbt_snowflake_version
ORDER BY last_seen DESC;
```
