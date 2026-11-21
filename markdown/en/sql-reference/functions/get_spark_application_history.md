Categories:
:   [Table functions](/sql-reference/functions-table)

# GET\_SPARK\_APPLICATION\_HISTORY

Returns the history of Snowpark Connect for Spark applications in the account, including batch jobs and client sessions. This is the
data that the [Spark Monitoring UI](/developer-guide/snowpark-connect/spark-monitoring-ui) displays.

## Syntax

Copy code

```
SNOWFLAKE.SNOWPARK_CONNECT.GET_SPARK_APPLICATION_HISTORY(
  [ CREATION_TIME_START => <constant_expr> ]
  [ , CREATION_TIME_END => <constant_expr> ]
  [ , RESULT_LIMIT => <integer> ] )
```

## Arguments

All arguments are optional.

`CREATION_TIME_START => constant_expr`
:   Start of the time range, in TIMESTAMP\_LTZ format, for the `CREATED_ON` time of the applications to return. For functions
    that you can use to construct a timestamp, see [Date & time functions](/sql-reference/functions-date-time).

`CREATION_TIME_END => constant_expr`
:   End of the time range, in TIMESTAMP\_LTZ format, for the `CREATED_ON` time of the applications to return.

`RESULT_LIMIT => integer`
:   Maximum number of rows to return. Must be a positive integer.

    If the number of matching rows exceeds the limit, the function returns the most recently created applications, up to
    the limit.

    Default: 100

## Output

The function returns one row per Spark application, with the following columns:

| Column | Data type | Description |
| --- | --- | --- |
| `ID` | VARCHAR | ID of the Spark application. For a batch job, this is the job ID (the query ID returned at submission). For a client session, this is the ID of the query that registered the session. |
| `NAME` | VARCHAR | Name of the application, such as the `app_name` passed to `init_spark_session`, the `EXECUTION_NAME` of a batch job, or the fully qualified name of a notebook. |
| `QUERY_ID` | VARCHAR | ID of the query that’s associated with the application. |
| `ACCOUNT_ID` | NUMBER | Internal ID of the account. |
| `CREATED_ON` | TIMESTAMP\_LTZ | Time when the application was created. |
| `STARTED_ON` | TIMESTAMP\_LTZ | Time when the application started running. |
| `COMPLETED_ON` | TIMESTAMP\_LTZ | Time when the application finished. NULL while the application is running. |
| `EXECUTION_STATUS` | VARCHAR | Status of the application: `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, or `CANCELLED`. |
| `ERROR_MESSAGE` | VARCHAR | Error message, if the application failed. |
| `OWNER` | VARCHAR | Name of the user who ran the application. Can be empty, for example for scheduled notebook runs. |
| `OWNER_ROLE_TYPE` | VARCHAR | Role that owns the application (for example, `SYSADMIN`). |
| `DATABASE_NAME` | VARCHAR | Database context of the application. |
| `DATABASE_ID` | NUMBER | Internal ID of the database. |
| `SCHEMA_NAME` | VARCHAR | Schema context of the application. |
| `SCHEMA_ID` | NUMBER | Internal ID of the schema. |
| `ERROR_CODE` | VARCHAR | Error code, if the application failed. |
| `EXIT_CODE` | NUMBER | Exit code of the application process, if available. |
| `ENVIRONMENT_RUNTIME_VERSION` | VARCHAR | Runtime version that the application ran on. |
| `ENTRYPOINT_FILE` | VARCHAR | Entry point file for a batch job. |
| `RESOURCE_CONSTRAINT` | VARCHAR | Resource constraint requested for the job. |
| `ARTIFACT_REPOSITORY` | VARCHAR | Artifact repository used to install packages. |
| `PACKAGES` | VARCHAR | Packages requested for the job. |
| `STAGE_MOUNTS` | VARCHAR | Stages mounted for the job. |
| `LOGS_STAGE_LOCATION` | VARCHAR | Stage location where job logs are written, if configured. |
| `EXTERNAL_ACCESS_INTEGRATIONS` | VARCHAR | External access integrations used by the job. |
| `SPARK_CONFIGURATION` | VARCHAR | Spark configuration properties set for the job. |
| `ARGUMENTS` | VARCHAR | Arguments passed to the job. |
| `DASHBOARD_URL` | VARCHAR | URL of the job’s dashboard, if available. |
| `MODE` | VARCHAR | How the application was run. See [Application modes](#label-get-spark-application-history-modes). |
| `SESSION_ID` | NUMBER | ID of the Snowflake session that ran the application. For a client session, all queries issued by the session have this session ID. |
| `EXECUTE_QUERY_ID` | VARCHAR | ID of the statement that started the batch job, if applicable. For `snowpark-submit` runs, this differs from `ID`. NULL for client sessions. |
| `COMMENT` | VARCHAR | Comment for the application. |
| `SPCS_SERVICE_NAME` | VARCHAR | Name of the Snowpark Container Services service that ran the application, if applicable. |
| `NOTEBOOK_PROJECT_OBJECT_NAME` | VARCHAR | Name of the notebook project object, for notebook runs. |
| `NPO_STORAGE_TYPE` | NUMBER | Storage type of the notebook project object, for notebook runs. |
| `NPO_FILE_DOMAIN_NAME` | VARCHAR | Domain name of the notebook file, for notebook runs. |
| `NPO_FILE_PATH` | VARCHAR | Path of the notebook file, for notebook runs. |
| `NPO_VERSION` | NUMBER | Version of the notebook project object, for notebook runs. |
| `EVENT_TABLE_ID` | NUMBER | Internal ID of the event table for the application. |
| `EVENT_TABLE_NAME` | VARCHAR | Fully qualified name of the event table for the application. |
| `WAREHOUSE_ID` | NUMBER | Internal ID of the warehouse that ran the application, if applicable. |
| `WAREHOUSE_NAME` | VARCHAR | Name of the warehouse that ran the application, if applicable. NULL for client sessions. |
| `COMPUTE_POOL_ID` | NUMBER | Internal ID of the compute pool that ran the application, if applicable. |
| `COMPUTE_POOL_NAME` | VARCHAR | Name of the compute pool that ran the application, if applicable. |

Expand

Show lessSee more

### Application modes

The `MODE` column identifies how the application was run:

| Mode | Description |
| --- | --- |
| `SCOS_CLIENT` | A Snowpark Connect for Spark client session, such as a session started from a local IDE. |
| `SCOS_SUBMIT` | A batch job run with `snowpark-submit`. |
| `SCOS_CODE_BUNDLE` | A batch job run with `EXECUTE CODE BUNDLE` with `type: spark`. |
| `SCOS_NOTEBOOK` | A scheduled notebook run that initialized a Snowpark Connect for Spark session. |

Expand

Show lessSee more

## Access control requirements

Usage on this function is granted to the `SNOWFLAKE.SNOWPARK_CONNECT_VIEWER` database role. This database role grants
usage on the function only. It doesn’t grant visibility into the applications of other users across the account. To
view other users’ applications, your role also needs account-level monitoring privileges. For example, an
[alert](/user-guide/alerts) that calls this function runs as the system user and returns no rows unless the alert owner
role has the MONITOR EXECUTION privilege on the account.

## Usage notes

- By default, the function returns applications created in the last 14 days. Applications created earlier aren’t
  returned, even if `CREATION_TIME_START` is set to an earlier time.
- To list the Snowflake queries issued by an application, pass its `ID` to
  `SNOWFLAKE.SNOWPARK_CONNECT.GET_SPARK_APPLICATION_QUERY_HISTORY`. For a client session, you can also join `SESSION_ID`
  to query history.
- Batch job logs, metrics, and traces are tagged with the application’s `EXECUTE_QUERY_ID` in the `snow.query.id`
  resource attribute of the event table. For `EXECUTE CODE BUNDLE` runs, `EXECUTE_QUERY_ID` and `ID` are the same
  value; for `snowpark-submit` runs, they differ. For more information, see
  [Filter event table records for a batch job](/developer-guide/snowpark-connect/snowpark-connect-monitoring#label-spconnect-filter-event-table).

## Examples

Return the 100 most recently created Spark applications:

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.SNOWPARK_CONNECT.GET_SPARK_APPLICATION_HISTORY());
```

Return applications that failed in the last seven days, with their error details:

Copy code

```
SELECT id, name, mode, owner, created_on, completed_on, error_code, error_message
FROM TABLE(SNOWFLAKE.SNOWPARK_CONNECT.GET_SPARK_APPLICATION_HISTORY(
    CREATION_TIME_START => DATEADD('day', -7, CURRENT_TIMESTAMP()),
    CREATION_TIME_END => CURRENT_TIMESTAMP(),
    RESULT_LIMIT => 1000))
WHERE execution_status = 'FAILED'
ORDER BY created_on DESC;
```

Return the client sessions started in the last day:

Copy code

```
SELECT id, name, owner, session_id, created_on
FROM TABLE(SNOWFLAKE.SNOWPARK_CONNECT.GET_SPARK_APPLICATION_HISTORY(
    CREATION_TIME_START => DATEADD('day', -1, CURRENT_TIMESTAMP())))
WHERE mode = 'SCOS_CLIENT'
ORDER BY created_on DESC;
```
