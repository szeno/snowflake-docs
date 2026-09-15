Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# DBT\_PROJECT\_EXECUTION\_HISTORY

Returns the execution history of [dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake).

Call this function to get metadata and results from past dbt Project executions within seven days of the current time. Optionally, specify the values to filter the results by.

Use this function with the following system functions to access dbt artifacts and logs programmatically:

- [SYSTEM$GET\_DBT\_LOG](/sql-reference/functions/system_get_dbt_log)
- [SYSTEM$LOCATE\_DBT\_ARCHIVE](/sql-reference/functions/system_locate_dbt_archive)
- [SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts)

For more information, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).

See also:
:   [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project), [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project), [DBT\_PROJECT\_EXECUTION\_HISTORY view](/sql-reference/account-usage/dbt_project_execution_history) (Account Usage)

## Syntax

Copy code

```
DBT_PROJECT_EXECUTION_HISTORY (
  [ OBJECT_NAME => '<name>' ]
  [ , OBJECT_TYPE = { WORKSPACE | DBT PROJECT }]
  [ , START_TIME_RANGE_START => <start_time> ]
  [ , START_TIME_RANGE_END => <end_time>  ]
  [ , RESULT_LIMIT = <integer> ]
  [ , COMMAND = <dbt_command> ]
  [ , USER_NAME = <user_name> ]
  [ , DATABASE = <db_name> ]
  [ , SCHEMA = <schema_name> ]
)
```

## Arguments

`OBJECT_NAME = <name>`
:   Name of the workspace or dbt project object that the execution belongs to.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`OBJECT_TYPE = { WORKSPACE | DBT PROJECT }`
:   The type of the object, WORKSPACE or DBT PROJECT, the execution belongs to.

`START_TIME_RANGE_START | START_TIME_RANGE_END = timestamp`
:   Timestamp to filter a range of executions.

`RESULT_LIMIT = integer`
:   An integer specifying the maximum number of rows returned by the function, from 1 - 10,000 inclusive.

    Default: 100

`COMMAND = dbt_command`
:   Specifies the [dbt command](https://docs.getdbt.com/reference/dbt-commands) used to execute the dbt project object.

`USER_NAME = user_name`
:   Name of the user that initiated the dbt project object execution.

`DATABASE = db_name`
:   Return only records for the specified database.

`SCHEMA = schema_name`
:   Return only records for the specified schema.

## Output

The function returns the following columns.

To view these columns, you must use a role with the MONITOR privilege.

| Column Name | Data Type | Description |
| --- | --- | --- |
| QUERY\_ID | TEXT | ID of the query. |
| QUERY\_START\_TIME | TIMESTAMP\_LTZ | The time the query started. |
| QUERY\_END\_TIME | TIMESTAMP\_LTZ | The time the query ended. |
| USER\_NAME | TEXT | The user that created the dbt project object. |
| OBJECT\_NAME | TEXT | Name of the workspace or dbt project object the execution belonged to. |
| OBJECT\_TYPE | TEXT | Type of object, such as WORKSPACE or DBT PROJECT. |
| DATABASE\_NAME | TEXT | Database of the object. |
| SCHEMA\_NAME | TEXT | Schema of the object. |
| COMMAND | TEXT | The command that was run for the object. |
| ARGS | TEXT | The arguments that were used in the run for the object. |
| ERROR\_CODE | NUMBER | If applicable, the error code for the run. |
| ERROR\_MESSAGE | TEXT | If applicable, error message stating why the run failed. |
| WAREHOUSE | TEXT | Warehouse used for the object. |
| STATE | TEXT | State of run, such as HANDLED\_ERROR or SUCCESS. |
| DBT\_VERSION | TEXT | The specific version used for this run. For example, `1.9.4`. |
| DBT\_SNOWFLAKE\_VERSION | TEXT | The specific dbt Projects on Snowflake version with patch version used for this run. For example, `1.9.4`. |

Expand

Show lessSee more

## Access control requirements

This table function includes only runs from workspaces and dbt Projects in which you have the following privileges:

- OWNERSHIP, READ, or WRITE on workspaces
- OWNERSHIP, USAGE, or MONITOR on dbt Projects

## Usage notes

- Use the exact dbt project object name (case-sensitive if created with quotes). If no row matches (wrong name or no executions yet), you might get an `Inputs may not be null.` error.
- Use function arguments such as `DATABASE`, `SCHEMA`, and `OBJECT_NAME` to filter results whenever possible. These filters are applied before the `RESULT_LIMIT` (default: 100 rows), so using them ensures you get the most relevant results rather than filtering a potentially truncated result set with a `WHERE` clause.

## Examples

The following example audits which engine version was used for recent runs:

Copy code

```
SELECT
    object_name,
    query_start_time,
    query_end_time,
    query_id,
    command,
    state
FROM TABLE (
    SNOWFLAKE.INFORMATION_SCHEMA.DBT_PROJECT_EXECUTION_HISTORY(
      DATABASE => 'ANALYTICS_DB',
      SCHEMA => 'DBT_PROD',
      OBJECT_NAME => 'FINANCE_ANALYTICS'
    )
  )
ORDER BY query_end_time DESC;
```

For detailed examples of using the DBT\_PROJECT\_EXECUTION\_HISTORY table function with system functions to access dbt artifacts and logs programmatically,
see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).
