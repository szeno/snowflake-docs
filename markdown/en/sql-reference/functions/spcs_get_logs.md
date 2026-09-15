Categories:
:   [Table functions](/sql-reference/functions-table) (Snowpark Container Services)

# <service\_name>!SPCS\_GET\_LOGS

Returns the logs that Snowflake collected from containers of the specified service. For more information, see [Publishing and accessing container logs](/developer-guide/snowpark-container-services/monitoring-services#label-snowpark-containers-working-with-services-local-logs).

See also:
:   [Monitoring Services](/developer-guide/snowpark-container-services/monitoring-services)

## Syntax

Copy code

```
<service_name>!SPCS_GET_LOGS(
  [ START_TIME => <constant_expr> ],
  [ END_TIME => <constant_expr> ] )
```

## Arguments

`START_TIME => constant_expr`
:   Start time (in TIMESTAMP\_LTZ format) for the time range from which to retrieve logs. For available functions to construct data, time, and timestamp data, see [Date & time functions](/sql-reference/functions-date-time).

    If the `START_TIME` isn’t specified, it defaults to 1 day ago.

`END_TIME => constant_expr`
:   End time (in TIMESTAMP\_LTZ format) for the time range from which to retrieve logs.

    If END\_TIME isn’t specified, it defaults to the current timestamp.

## Output

Each row in the output corresponds to one logged event in the event table.
Each line that your service outputs to `stdout` or `stderr` results in one row in the output.

The function returns the following columns:

| Column | Data Type | Description |
| --- | --- | --- |
| `TIMESTAMP` | TIMESTAMP\_NTZ | Universal Coordinated Time (UTC) timestamp when Snowflake collected the log from the container. This value maps to the TIMESTAMP column in the event table. |
| `INSTANCE_ID` | NUMBER | ID of the job service instance. This value maps to the `snow.service.instance` field in the RESOURCE\_ATTRIBUTES column in the event table. |
| `CONTAINER_NAME` | VARCHAR | Name of the container. This value maps to the `snow.service.container.name` field in the RESOURCE\_ATTRIBUTES column in the event table. |
| `LOG` | VARCHAR | Log Snowflake collected from your application container. This value maps to the VALUE column in the event table. |
| `RECORD_ATTRIBUTES` | OBJECT | Additional information about the log. For example, the log stream — stderr or stdout — from where the log was collected. This value maps to the RECORD\_ATTRIBUTES column in the event table. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MONITOR | Service |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- It can take a few minutes before your container logs show in the output.

## Examples

Retrieve the logs that Snowflake collected from containers of the `my_test_job` job over the past day.

Copy code

```
SELECT * FROM TABLE(mydb.myschema.my_test_job!SPCS_GET_LOGS());
```

Example output:

```
+-------------------------+-------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------+
| TIMESTAMP               | INSTANCE_ID | CONTAINER_NAME | LOG                                                                                                                                                                 | RECORD_ATTRIBUTES          |
|-------------------------+-------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------|
| 2025-06-26 00:23:40.281 |           0 | main           | job-tutorial - INFO - Job finished                                                                                                                                  | {                          |
|                         |             |                |                                                                                                                                                                     |   "log.iostream": "stdout" |
|                         |             |                |                                                                                                                                                                     | }                          |
| 2025-06-26 00:23:38.787 |           0 | main           | job-tutorial - INFO - Executing query [select current_time() as time,'hello'] and writing result to table [results]                                                 | {                          |
|                         |             |                |                                                                                                                                                                     |   "log.iostream": "stdout" |
|                         |             |                |                                                                                                                                                                     | }                          |
| 2025-06-26 00:23:38.787 |           0 | main           | job-tutorial - INFO - Connection succeeded. Current session context: database="TUTORIAL_DB", schema="DATA_SCHEMA", warehouse="TUTORIAL_WAREHOUSE", role="TEST_ROLE" | {                          |
|                         |             |                |                                                                                                                                                                     |   "log.iostream": "stdout" |
|                         |             |                |                                                                                                                                                                     | }                          |
| 2025-06-26 00:23:36.852 |           0 | main           | job-tutorial - INFO - Job started                                                                                                                                   | {                          |
|                         |             |                |                                                                                                                                                                     |   "log.iostream": "stdout" |
|                         |             |                |                                                                                                                                                                     | }                          |
+-------------------------+-------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------+
```

Retrieve the logs that Snowflake collected from containers of the `my_test_job` job over the past three days.

Copy code

```
SELECT * FROM TABLE(mydb.myschema.my_test_job!SPCS_GET_LOGS(START_TIME => DATEADD('day', -3, CURRENT_TIMESTAMP())));
```

Retrieve the logs for the `my_test_job` job instance `0` in the container named `main`. As shown in the following example, if you omit the START\_TIME and END\_TIME arguments, the function retrieves the logs for the past day:

Copy code

```
SELECT * FROM TABLE(mydb.myschema.my_test_job!SPCS_GET_LOGS())
WHERE instance_id = 0 AND container_name = 'main';
```
