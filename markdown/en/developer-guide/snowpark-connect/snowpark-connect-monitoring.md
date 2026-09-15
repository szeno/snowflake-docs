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
  AND RESOURCE_ATTRIBUTES['snow.service.container.name'] = '"server"'
  AND RECORD_TYPE = 'LOG'
ORDER BY timestamp;

-- Client-side logs only
SELECT timestamp, VALUE::string AS log_line
FROM MY_DB.PUBLIC.my_event_table
WHERE timestamp BETWEEN <start> AND <end>
  AND RESOURCE_ATTRIBUTES['snow.service.name'] = '<workload_name>'
  AND RESOURCE_ATTRIBUTES['snow.service.container.name'] = '"client"'
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
