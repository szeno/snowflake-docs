Categories:
:   [Table functions](/sql-reference/functions-table)

# GET\_JOB\_HISTORY

Returns the job history for [Snowpark Container Services jobs](/developer-guide/snowpark-container-services/working-with-services) up to 30 days with an optional time range. The function returns both running and deleted jobs.

See also:
:   [Run a job service](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-creating-job)

## Syntax

Copy code

```
SNOWFLAKE.SPCS.GET_JOB_HISTORY(
  [ CREATED_TIME_START => <constant_expr> ],
  [ CREATED_TIME_END => <constant_expr> ],
  [ RESULT_LIMIT = <integer> ])
```

## Arguments

`CREATED_TIME_START => constant_expr`
:   Start time, in TIMESTAMP\_LTZ format — for example, ’2024-04-05 01:02:03’ — for the time range when jobs were created to retrieve the job history. For available functions to construct data, time, and timestamp data, see [Date & time functions](/sql-reference/functions-date-time).

    Default: 30 days from the current timestamp.

`CREATED_TIME_END => constant_expr`
:   End time, in TIMESTAMP\_LTZ format, for the time range to retrieve the job history.

    Default: Current timestamp.

`RESULT_LIMIT => integer`
:   Maximum number of rows to return.

    If the number of matching rows exceeds the specified limit, only the jobs with the most recent timestamps are returned, up to the specified limit.

    Range: 1 to 10000

    Default: 100

## Output

The function returns the following columns:

| Column | Data Type | Description |
| --- | --- | --- |
| `QUERY_ID` | VARCHAR | ID of the EXECUTE JOB SERVICE SQL statement. |
| `ID` | NUMBER | Internal/system-generated identifier for the job. |
| `NAME` | VARCHAR | Name of the job. |
| `DATABASE_NAME` | VARCHAR | Name of the database in which the job is created. |
| `SCHEMA_NAME` | VARCHAR | Name of the schema in which the job is created. |
| `CREATED_TIME` | TIMESTAMP\_LTZ | Time when the job was created. |
| `COMPLETED_TIME` | TIMESTAMP\_LTZ | Time when the job was completed. |
| `DELETED_TIME` | TIMESTAMP\_LTZ | Time when the job was deleted. |
| `STATUS` | VARCHAR | Staus of the job. |
| `MESSAGE` | VARCHAR | Additional information about the job status. |
| `INSTANCE_STATUSES` | OBJECT | Key-value pairs that describe job instances and containers. |
| `COMPUTE_POOL_NAME` | VARCHAR | Name of the compute pool where the job was run. |
| `OWNER` | VARCHAR | Role that owns the job. |
| `OWNER_ROLE_TYPE` | VARCHAR | Type of role that owns the job, either ROLE or DATABASE\_ROLE. |
| `PARAMETERS` | OBJECT | Key-value pairs that describe the parameters that were specified when the job was created. |
| `MANAGING_OBJECT` | OBJECT | Key-value pairs that describe the managing object. NULL if the job isn’t managed by Snowflake. |

Expand

Show lessSee more

## Access control requirements

The PUBLIC role has the privilege to use this function.

Everyone can call this function, but the output depends on the current role.
The output only includes the jobs that are owned by the current role.

## Examples

- Returns the job history of all jobs created by the current role within the last 30 days
  (the default *CREATED\_TIME\_START* value).

  Copy code

  ```
  SELECT * FROM TABLE(SNOWFLAKE.SPCS.GET_JOB_HISTORY(());
  ```

  The following example output shows only one job:

  ```
  +--------------------------------------+-----+-------------+---------------+-------------+-------------------------------+-------------------------------+--------------+--------+-----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------+-----------+-----------------+-----------------+-----------------+
  | QUERY_ID                             |  ID | NAME        | DATABASE_NAME | SCHEMA_NAME | CREATED_TIME                  | COMPLETED_TIME                | DELETED_TIME | STATUS | MESSAGE                     | INSTANCE_STATUSES                                                                                                                                               | COMPUTE_POOL_NAME     | OWNER     | OWNER_ROLE_TYPE | PARAMETERS      | MANAGING_OBJECT |
  |--------------------------------------+-----+-------------+---------------+-------------+-------------------------------+-------------------------------+--------------+--------+-----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------+-----------+-----------------+-----------------+-----------------|
  | 01bd46d2-0004-be62-0000-ff07016490a6 | 131 | MY_TEST_JOB | TUTORIAL_DB   | DATA_SCHEMA | 2025-06-25 17:50:00.728 -0700 | 2025-06-25 17:50:10.515 -0700 | NULL         | DONE   | Job completed successfully. | {                                                                                                                                                               | TUTORIAL_COMPUTE_POOL | TEST_ROLE | ROLE            | {               | NULL            |
  |                                      |     |             |               |             |                               |                               |              |        |                             |   "failedInstances": 0,                                                                                                                                         |                       |           |                 |   "ASYNC": true |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |   "instances": [                                                                                                                                                |                       |           |                 | }               |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |     {                                                                                                                                                           |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |       "containers": [                                                                                                                                           |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |         {                                                                                                                                                       |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |           "containerName": "main",                                                                                                                              |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |           "image": "org-account.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_job_image:latest",                               |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |           "imageSha256": "sha256:ff07f19f233cfe76a889e39d9d7098d528312acc789f1c0cf929556a56c61a9a",                                                             |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |           "lastExitCode": 0,                                                                                                                                    |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |           "message": "Completed successfully",                                                                                                                  |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |           "restartCount": 0,                                                                                                                                    |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |           "startTime": "",                                                                                                                                      |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |           "status": "DONE"                                                                                                                                      |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |         }                                                                                                                                                       |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |       ],                                                                                                                                                        |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |       "instanceId": "0"                                                                                                                                         |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |     }                                                                                                                                                           |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |   ],                                                                                                                                                            |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |   "pendingInstances": 0,                                                                                                                                        |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |   "runningInstances": 0,                                                                                                                                        |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |   "succeededInstances": 1,                                                                                                                                      |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             |   "totalInstances": 1                                                                                                                                           |                       |           |                 |                 |                 |
  |                                      |     |             |               |             |                               |                               |              |        |                             | }                                                                                                                                                               |                       |           |                 |                 |                 |
  +--------------------------------------+-----+-------------+---------------+-------------+-------------------------------+-------------------------------+--------------+--------+-----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------+-----------+-----------------+-----------------+-----------------+
  ```
- Returns the job history of up to 10 jobs that are owned by the current role that ran within the last three days.

  Copy code

  ```
  SELECT *
   FROM TABLE(snowflake.spcs.get_job_history(
           result_limit => 10,
           created_time_start => dateadd('day', -3, current_timestamp())
    ));
  ```
- Retrieves up to 10 jobs that ran between three days ago and one day ago, not including today.

  Copy code

  ```
  SELECT * FROM TABLE(SNOWFLAKE.SPCS.GET_JOB_HISTORY(
  RESULT_LIMIT => 10,
  CREATED_TIME_START => DATEADD('day', -3, CURRENT_TIMESTAMP()),
  CREATED_TIME_END => DATEADD('day', -1, CURRENT_TIMESTAMP())));
  ```
