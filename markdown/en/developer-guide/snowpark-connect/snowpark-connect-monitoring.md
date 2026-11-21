# Monitoring Snowpark Connect for Spark workloads

Snowpark Connect for Spark uses Python’s standard `logging` module for diagnostics. When running workloads through
[snowpark-submit](/developer-guide/snowpark-connect/snowpark-connect-using-submit), logs are
written to your account’s
[event table](/developer-guide/logging-tracing/event-table-setting-up), giving you full
SQL-queryable access to server and client output.

## Log levels

Snowpark Connect for Spark emits logs at two primary levels:

`INFO`
:   Summarizes high-level operations: session creation, query execution, UDF registration, and
    configuration changes. This is the default and is sufficient for most monitoring.

`DEBUG`
:   Adds detailed internal state: generated SQL, plan translation steps, gRPC message details, and
    cache decisions. Use this level when you need to inspect the exact queries sent to Snowflake or
    diagnose unexpected behavior.

## Configuring log output for local and notebook environments

When running the Snowpark Connect for Spark server locally (through `init_spark_session`), configure the logger
**before** importing and starting the session:

Copy code

```
import logging

logging.getLogger("snowflake_connect_server").setLevel(logging.DEBUG)

from snowflake.snowpark_connect import init_spark_session

spark = init_spark_session()
```

Snowflake Notebooks don’t display Python log output by default. To see Snowpark Connect for Spark logs in the
notebook cell output, attach a `StreamHandler` to the logger:

Copy code

```
import logging

logger = logging.getLogger("snowflake_connect_server")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(handler)

from snowflake.snowpark_connect import init_spark_session

spark = init_spark_session()
```

![Snowpark Connect log output in a Snowflake Notebook](/static/images/snowpark-connect/notebook-logging.png)

## Event table logs for Snowpark Submit

When you run workloads through snowpark-submit, the SCOS server and client containers write logs,
OpenTelemetry spans, and resource metrics to your account’s event table. This is the primary way to
monitor production workloads.

### Prerequisites

- An event table configured in your account. Verify with:

  Copy code

  ```
  SHOW PARAMETERS LIKE 'EVENT_TABLE' IN ACCOUNT;
  ```

  For setup instructions, see
  [Event table overview](/developer-guide/logging-tracing/event-table-setting-up).

Note

Database-level event tables are not supported. Logs from Snowpark Submit workloads are written only to the account-level event table.

### Retrieving logs via the CLI

Use the `--workload-status` and `--display-logs` flags to retrieve logs from a completed or
running job. The full workload name (with a UTC timestamp suffix) is printed when you submit:

Copy code

```
# Last 100 lines (default)
snowpark-submit \
  --snowflake-workload-name <workload_name> \
  --workload-status \
  --display-logs \
  --snowflake-connection-name my_connection

# Last 500 lines
snowpark-submit \
  --snowflake-workload-name <workload_name> \
  --workload-status \
  --display-logs \
  --number-of-most-recent-log-lines 500 \
  --snowflake-connection-name my_connection

# All logs
snowpark-submit \
  --snowflake-workload-name <workload_name> \
  --workload-status \
  --display-logs \
  --number-of-most-recent-log-lines -1 \
  --snowflake-connection-name my_connection
```

### Querying logs with SQL

For full control over filtering and analysis, query the event table directly.

**Get all log lines for a job:**

Copy code

```
SELECT timestamp, VALUE::string AS log_line
FROM MY_DB.PUBLIC.my_event_table
WHERE timestamp BETWEEN '2026-04-17 10:24:00'::timestamp_tz
                     AND '2026-04-17 10:40:00'::timestamp_tz
  AND RESOURCE_ATTRIBUTES['snow.service.name'] = '<workload_name>'
  AND RECORD_TYPE = 'LOG'
ORDER BY timestamp;
```

Tip

Always include a timestamp range. The event table can have millions of rows per day; without a
time bound, queries are very slow or time out.

**Filter by container:**

Each job has two containers: `server` (SCOS internals, SQL execution) and `client` (your
PySpark app output).

Copy code

```
-- Server-side logs only
SELECT timestamp, VALUE::string AS log_line
FROM MY_DB.PUBLIC.my_event_table
WHERE timestamp BETWEEN <start> AND <end>
  AND RESOURCE_ATTRIBUTES['snow.service.name'] = '<workload_name>'
  AND RESOURCE_ATTRIBUTES['snow.service.container.name'] = 'server'
  AND RECORD_TYPE = 'LOG'
ORDER BY timestamp;

-- Client-side logs only
SELECT timestamp, VALUE::string AS log_line
FROM MY_DB.PUBLIC.my_event_table
WHERE timestamp BETWEEN <start> AND <end>
  AND RESOURCE_ATTRIBUTES['snow.service.name'] = '<workload_name>'
  AND RESOURCE_ATTRIBUTES['snow.service.container.name'] = 'client'
  AND RECORD_TYPE = 'LOG'
ORDER BY timestamp;
```

**Filter by severity:**

Available severity values: `DEBUG`, `INFO`, `WARN`, and `None` (unstructured output that
doesn’t go through Python’s logging module).

Copy code

```
SELECT timestamp,
       RECORD['severity_text']::string AS severity,
       VALUE::string AS log_line
FROM MY_DB.PUBLIC.my_event_table
WHERE timestamp BETWEEN <start> AND <end>
  AND RESOURCE_ATTRIBUTES['snow.service.name'] = '<workload_name>'
  AND RECORD_TYPE = 'LOG'
  AND RECORD['severity_text']::string IN ('INFO', 'WARN')
ORDER BY timestamp;
```

## Query Spark application history with SQL

The [Spark Monitoring UI](/developer-guide/snowpark-connect/spark-monitoring-ui) reads from the
[GET\_SPARK\_APPLICATION\_HISTORY](/sql-reference/functions/get_spark_application_history) table function. You can call
this function directly to build your own reports, find failed runs, or trace an application back to its queries and
event table records. Each row describes one application, and the `MODE` column identifies whether it’s a client
session (`SCOS_CLIENT`), a `snowpark-submit` job (`SCOS_SUBMIT`), an `EXECUTE CODE BUNDLE` job (`SCOS_CODE_BUNDLE`), or
a scheduled notebook run (`SCOS_NOTEBOOK`). By default, the function returns applications created in the last 14 days.
For the full syntax and list of output columns, see
[GET\_SPARK\_APPLICATION\_HISTORY](/sql-reference/functions/get_spark_application_history).

### Examples

List applications that failed in the last seven days, with their error details:

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

Count runs and average duration by mode and status over the last 14 days:

Copy code

```
SELECT mode,
       execution_status,
       COUNT(*) AS runs,
       AVG(DATEDIFF('second', started_on, completed_on)) AS avg_duration_seconds
FROM TABLE(SNOWFLAKE.SNOWPARK_CONNECT.GET_SPARK_APPLICATION_HISTORY(
    CREATION_TIME_START => DATEADD('day', -14, CURRENT_TIMESTAMP()),
    RESULT_LIMIT => 10000))
GROUP BY mode, execution_status
ORDER BY mode, execution_status;
```

### Find the queries issued by an application

To list the Snowflake queries issued by an application, pass its `ID` to
`SNOWFLAKE.SNOWPARK_CONNECT.GET_SPARK_APPLICATION_QUERY_HISTORY`. This works for client sessions (`SCOS_CLIENT`) as well
as batch jobs, and is the main way to trace a client session’s work back to Snowflake queries:

Copy code

```
SELECT query_id, query_text, execution_status, start_time, total_elapsed_time
FROM TABLE(SNOWFLAKE.SNOWPARK_CONNECT.GET_SPARK_APPLICATION_QUERY_HISTORY('<application_id>'))
ORDER BY start_time;
```

The results include the queries generated by your DataFrame operations, along with setup queries that Snowpark Connect for Spark runs
when the session starts (for example, `ALTER SESSION` statements).

You can also use the `SESSION_ID` column to join a client session to query history. For example, to find the session’s
queries in [QUERY\_HISTORY\_BY\_SESSION](/sql-reference/functions/query_history):

Copy code

```
SELECT query_id, query_text, execution_status, start_time
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY_BY_SESSION(
    SESSION_ID => <session_id>,
    RESULT_LIMIT => 1000))
ORDER BY start_time;
```

### Filter event table records for a batch job

Batch jobs (`SCOS_SUBMIT`, `SCOS_CODE_BUNDLE`, and `SCOS_NOTEBOOK`) write their logs, metrics, and traces to an event table, which is
named in the `EVENT_TABLE_NAME` column. Client sessions (`SCOS_CLIENT`) don’t write application logs or metrics to an
event table, because that code runs on the client. To trace a client session, use
[its query history](#label-spconnect-application-queries) instead.

To retrieve the event table records for one batch job:

1. Look up the event table and the time window for the application:

   Copy code

   ```
   SELECT id, execute_query_id, event_table_name, created_on, completed_on
   FROM TABLE(SNOWFLAKE.SNOWPARK_CONNECT.GET_SPARK_APPLICATION_HISTORY(RESULT_LIMIT => 1000))
   WHERE name = 'my_app_name'
   ORDER BY created_on DESC;
   ```
2. Query that event table, filtering on the application’s `EXECUTE_QUERY_ID`. Records are tagged with this value in the
   `snow.query.id` resource attribute. For `EXECUTE CODE BUNDLE` runs, `EXECUTE_QUERY_ID` is the same as `ID`; for
   `snowpark-submit` runs, it’s different, so always use `EXECUTE_QUERY_ID`. Spans for the individual queries that the
   job issued carry those queries’ own IDs in `snow.query.id`, so they aren’t included in this filter.

   Filtering on `timestamp` with the application’s `CREATED_ON` and `COMPLETED_ON` values limits how much of the event
   table Snowflake has to scan. The event table `timestamp` column is in UTC, so convert the window to UTC. A running
   job has a NULL `COMPLETED_ON`, so use the current time as the end of the window until the job finishes:

   Copy code

   ```
   WITH app AS (
     SELECT execute_query_id, created_on, completed_on
     FROM TABLE(SNOWFLAKE.SNOWPARK_CONNECT.GET_SPARK_APPLICATION_HISTORY(RESULT_LIMIT => 1000))
     WHERE id = '<application_id>'
   )
   SELECT e.timestamp,
          e.record_type,
          e.record['severity_text']::STRING AS severity,
          e.value
   FROM my_db.my_schema.my_event_table e, app
   WHERE e.resource_attributes['snow.query.id'] = app.execute_query_id
     AND e.timestamp BETWEEN CONVERT_TIMEZONE('UTC', app.created_on)::TIMESTAMP_NTZ
                         AND CONVERT_TIMEZONE('UTC', COALESCE(app.completed_on, CURRENT_TIMESTAMP()))::TIMESTAMP_NTZ
   ORDER BY e.timestamp;
   ```

   To return only log messages, add `AND e.record_type = 'LOG'`. To return only trace spans, use `e.record_type = 'SPAN'`.

You need privileges to query the event table. For more information, see
[Event table overview](/developer-guide/logging-tracing/event-table-setting-up).

### Send an email notification when a batch job fails

You can combine GET\_SPARK\_APPLICATION\_HISTORY with an [alert](/user-guide/alerts) and
[email notifications](/user-guide/notifications/email-notifications) to get an email whenever a batch job fails.

1. Create an email notification integration. Recipients must be users in your account who have
   [verified their email addresses](/user-guide/notifications/email-notifications#label-email-notification-verify-address).
   Creating a notification integration requires the CREATE INTEGRATION or CREATE NOTIFICATION INTEGRATION privilege:

   Copy code

   ```
   CREATE NOTIFICATION INTEGRATION spark_job_email_int
     TYPE = EMAIL
     ENABLED = TRUE
     ALLOWED_RECIPIENTS = ('first.last@example.com');
   ```
2. Grant the privileges that the alert’s owner role needs. The alert runs as a system user, so the owner role needs the
   MONITOR EXECUTION privilege to see applications run by other users. Without it, the function returns no rows inside
   the alert and the alert never fires:

   Copy code

   ```
   GRANT USAGE ON INTEGRATION spark_job_email_int TO ROLE my_alert_role;
   GRANT EXECUTE ALERT ON ACCOUNT TO ROLE my_alert_role;
   GRANT MONITOR EXECUTION ON ACCOUNT TO ROLE my_alert_role;
   ```
3. Create the alert. Every five minutes, the alert checks for batch jobs that failed since the last time the alert ran,
   and sends one email that lists them:

   Copy code

   ```
   CREATE OR REPLACE ALERT my_db.my_schema.spark_job_failure_alert
     WAREHOUSE = my_warehouse
     SCHEDULE = '5 MINUTE'
     IF (EXISTS (
       SELECT name, mode, owner, completed_on, error_message
       FROM TABLE(SNOWFLAKE.SNOWPARK_CONNECT.GET_SPARK_APPLICATION_HISTORY(
           CREATION_TIME_START => DATEADD('day', -1, SNOWFLAKE.ALERT.SCHEDULED_TIME()),
           RESULT_LIMIT => 10000))
       WHERE execution_status = 'FAILED'
         AND mode <> 'SCOS_CLIENT'
         AND completed_on > SNOWFLAKE.ALERT.LAST_SUCCESSFUL_SCHEDULED_TIME()
         AND completed_on <= SNOWFLAKE.ALERT.SCHEDULED_TIME()
     ))
     THEN
       BEGIN
         LET failed_jobs VARCHAR := (
           SELECT LISTAGG(name || ' (' || mode || ', owner: ' || COALESCE(owner, 'n/a') || '): '
                          || COALESCE(error_message, 'no error message'), '\n')
           FROM TABLE(RESULT_SCAN(SNOWFLAKE.ALERT.GET_CONDITION_QUERY_UUID()))
         );
         CALL SYSTEM$SEND_EMAIL(
           'spark_job_email_int',
           'first.last@example.com',
           'Snowpark Connect job failed',
           'The following Spark jobs failed:\n' || :failed_jobs
         );
       END;
   ```

   The action uses [GET\_CONDITION\_QUERY\_UUID](/sql-reference/functions/get_condition_query_uuid) to read the failed jobs
   that the condition returned, so the email lists each job’s name, mode, owner, and error message. Filtering on
   `COMPLETED_ON` between [LAST\_SUCCESSFUL\_SCHEDULED\_TIME](/sql-reference/functions/last_successful_scheduled_time) and
   [SCHEDULED\_TIME](/sql-reference/functions/scheduled_time) reports each failure once. On the alert’s first run,
   it reports failures from the last day.
4. Resume the alert. New alerts are suspended:

   Copy code

   ```
   ALTER ALERT my_db.my_schema.spark_job_failure_alert RESUME;
   ```

To check that the alert ran and sent the email, query
[ALERT\_HISTORY](/sql-reference/functions/alert_history) and
[NOTIFICATION\_HISTORY](/sql-reference/functions/notification_history). For other ways to send notifications, such as
to a webhook, see [Sending notifications to external systems](/user-guide/notifications/about-notifications).

## Viewing generated queries in Snowsight

Every SQL statement that Snowpark Connect for Spark sends to Snowflake is visible in the
[Snowsight query history](/user-guide/ui-snowsight-activity). To find queries from your
workload:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) and go to **Monitoring** » **Query History**.
2. Filter by the warehouse your Snowpark Connect for Spark session uses.
3. If you set `spark.app.name`, filter by **Query Tag** containing
   `Spark-Connect-App-Name=<your app name>`.

This lets you inspect the exact SQL that Snowpark Connect for Spark generated, review execution times, and
identify slow queries. You can also use the
[QUERY\_HISTORY view](/sql-reference/account-usage/query_history) for programmatic analysis.
