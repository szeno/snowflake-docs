# Spark Monitoring UI

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Spark Monitoring UI provides a view of Snowpark Connect for Spark usage and history across your Snowflake account. This UI consolidates the relevant information from each Snowpark Connect for Spark job or interactive session to aid in monitoring and troubleshooting.

Batch jobs from `snowpark-submit` and `EXECUTE CODE BUNDLE` appear under the **Batch Jobs** tab. That includes Spark jobs whose specification sets `type: spark`, and scheduled notebooks that initialize a Snowpark Connect session. Each run shows status, duration, name, and owner. Any Snowpark Connect session connection is tracked under the **Spark Sessions** tab with its queries and owner.

![Spark Monitoring UI showing batch jobs in the account.](/static/images/snowpark-connect/spark-home-page.png)

The following sections cover how to open the page and how each tab behaves.

## Open Spark Monitoring UI

1. Sign in to Snowsight.
2. Select **Monitoring** » **Spark**.

![Navigate to Spark by going to Monitoring from the home page.](/static/images/snowpark-connect/spark-navigation.png)

## Batch Jobs Tab

The **Batch Jobs** tab lists three kinds of batch-style Snowpark Connect for Spark executions for your account:

- [`snowpark-submit`](/developer-guide/snowpark-connect/snowpark-connect-using-submit) runs
- [`EXECUTE CODE BUNDLE`](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle) runs whose specification sets `type: spark`
- [`EXECUTE CODE BUNDLE`](/developer-guide/snowpark-connect/snowpark-connect-submit-notebook-code-bundle) runs for scheduled notebooks that initialize a Snowpark Connect session

For each run you can see duration, who submitted the job, and status.

### Batch Job Details Page

Select a row to open the details view for that run. The details include:

- The `snowpark-submit` command line or the SQL command that was executed
- Queries associated with the job
- Log output
- An OpenTelemetry trace for the job

For log and event-table behavior for submit workloads, see [Monitoring Snowpark Connect for Spark workloads](/developer-guide/snowpark-connect/snowpark-connect-monitoring).

Note

The **Logs** section shows log records that were ingested into your event table, which is controlled by the `LOG_LEVEL`
parameter. Set `LOG_LEVEL` to any level other than `OFF` and the **Logs** section shows records at that level and more
severe — for example, `INFO` shows `INFO`, `WARN`, `ERROR`, and `FATAL`, while `WARN` shows `WARN` and more severe. Set
`LOG_LEVEL` at the scope that matches your event table: at the **account** level if you use an account-level event
table, or at the **database** level if the job’s database uses a database-level event table. If `LOG_LEVEL` is `OFF`,
the **Logs** section is empty even when the run succeeds. For more information, see
[Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

![The details page for a batch job shows the status, duration, logs, and queries.](/static/images/snowpark-connect/spark-batch-details.png)

#### Batch Job Trace Tab

The **Trace** tab on the Details page shows an OpenTelemetry trace of the job execution. Each DataFrame action is represented by a span, and the associated queries for each of those DataFrame actions is shown as a child span. This can help you more easily visualize the portions of your job that are taking the longest to run, and more easily get to the Query Profile for any slow or failed DataFrame actions.

For how trace data is represented and how to view or query it in your event table, see [Viewing trace data](/developer-guide/logging-tracing/tracing-accessing-events).

![The Trace tab shows the end to end trace of the job.](/static/images/snowpark-connect/spark-batch-trace.png)

## Spark Sessions Tab

The **Spark Sessions** tab lists Snowpark Connect for Spark client sessions that have connected to your account. That includes sessions from local laptops, Snowflake Notebooks, Snowflake Workspaces, and other supported clients.

For each session, Snowsight shows when the session started, who started it, the session ID, and the **session name**.

![The Spark Sessions tab lists active and recent Spark sessions for the account.](/static/images/snowpark-connect/spark-sessions-tab.png)

## Spark Session Details Page

The details page for a Spark Session shows all of the Queries issued from that session. Clicking the Query ID for one of these queries will take you to the Query Profile, which you can use to debug long or failed queries.

![The Spark Session details page lists queries issued from the session.](/static/images/snowpark-connect/spark-session-details.png)

### Setting the App Name

The app name comes from the `app_name` argument when you call `init_spark_session`. If you set `app_name`, that value appears as the session name in Snowsight.

Copy code

```
from snowflake.snowpark_connect import init_spark_session

init_spark_session(app_name="my_app_name")
```

In this example, `my_app_name` is shown as the session name.

If you do not pass `app_name`, Snowpark Connect uses the file name where the session was created as the `app_name` (for example `main.py`). For how the Python API derives the default application name, see the `app_name` parameter on [init\_spark\_session](/developer-guide/snowpark-connect/snowpark-connect-reference#label-spconnect-ref-init-spark-session).

## Limitations

- For a scheduled Snowflake Notebook run (`EXECUTE CODE BUNDLE` with `type: custom`), the run only appears in the **Batch Jobs** tab once the notebook code calls `snowflake.snowpark_connect.init_spark_session()` to start a Snowpark Connect session. If your notebook initializes the session late in its execution, there can be a lag between when the notebook actually starts and when Snowpark Connect for Spark registers it as a Spark job in **Batch Jobs**.
