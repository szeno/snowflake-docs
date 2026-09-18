# Observability and logging for Notebooks in Workspaces

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

## Overview

Snowflake writes notebook logs to the container’s local file system and ingests them into an [event table](/developer-guide/logging-tracing/event-table-setting-up), which you can query to troubleshoot notebook runs, review execution history, and perform long-term analysis.

You can use an event table to centralize operational data for Notebooks in Workspaces; for example, with the following tasks:

- Troubleshooting scheduled runs (errors, warnings, timestamps)
- Auditing who ran what and when (when emitted by the workload and configured for collection)
- Creating dashboards for notebook activity (success/failure counts, run duration, noisy errors)

Note

There is typically a delay of three to five minutes before logs appear in the event table.

## Enable logging in your notebook code

By default, Python logging is set to `WARNING`. To capture application events, you must set the logging level to `INFO` or
`DEBUG`.

- Add the following code to your Python notebook or script:

Copy code

```
import logging

# Set the root logger to INFO level
logging.getLogger().setLevel(logging.INFO)

# Generate a test log entry
logging.info("APPLICATION_EVENT: Service initialization complete.")
```

## Query logs using Snowflake Trail

You can view log entries in Snowsight through Snowflake Trail.

Note

Before you can view log messages, you must [enable telemetry data collection](/developer-guide/logging-tracing/logging-tracing-enabling).

### Identify your event table

- To find the event table for your account, run the following command in a SQL file:

Copy code

```
SHOW PARAMETERS LIKE 'event_table' IN ACCOUNT;
```

### Query and analyze logs

After your event table has started collecting events, you can query it like any other table to filter by time range, severity, and workload identifiers.
For more information on event table schema and column definitions, see [Event table columns](/developer-guide/logging-tracing/event-table-columns).

- To investigate recent log events, run the following code (replacing the placeholder values with your actual values):

  Copy code

  ```
  SELECT
   TIMESTAMP,
   VALUE AS LOG_MESSAGE,
   RESOURCE_ATTRIBUTES:"snow.service.name"::string AS SERVICE_NAME,
   RECORD:"severity_text"::string AS SEVERITY
  FROM <database_name>.<schema_name>.<event_table_name>
  WHERE RECORD_TYPE = 'LOG'
    AND RESOURCE_ATTRIBUTES:"snow.service.name" = '<your_service_name>'
    AND TIMESTAMP > DATEADD(hour, -1, CURRENT_TIMESTAMP())
  ORDER BY TIMESTAMP DESC
  LIMIT 100;
  ```

## View logs for scheduled notebook runs in Snowsight

Each scheduled notebook uses a Code Bundle (formerly a Notebook Project Object) that stores deployed code, execution history, and artifacts.

To view logs for scheduled runs in Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Explorer**.
3. Search for the database and schema containing the Code Bundle.
4. Select the Code Bundle, and then select the **Run history** tab.
5. For the run you want to inspect, in the **Logs** column, select **Logs**.

After you enable logging in your notebook code, your custom log messages and infrastructure initialization logs appear in this log view.

## Understand scheduled run failures

When a scheduled, non-interactive run fails, Snowflake reports a categorized reason so you can tell what went wrong and where to look next. Failures
fall into two categories:

- **System errors:** a failure in the Snowflake-managed infrastructure that runs the notebook, such as the kernel not becoming ready in time, a lost
  connection, or a workspace file sync failure. System errors are prefixed with `[Internal error]` and are associated with error code `505186`.
- **User errors:** a failure caused by the notebook’s code or configuration, such as a cell that failed or timed out, a notebook file that wasn’t
  found, an unsupported notebook format, or a package installation that failed. User errors are associated with error code `505187`.

The categorized reason appears in the run’s error details. To investigate further, review the run’s logs and run history:

- For the run history and result visibility of scheduled runs, see
  [Run and schedule Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule).
- To query logs for the same time window, use your event table as described in [Query logs using Snowflake Trail](#query-logs-using-snowflake-trail).

## Troubleshooting

- If you don’t see expected events, verify that your event table is created and that event logging is enabled and configured for your account and
  workloads.
- If scheduled runs fail, cross-check [notebook scheduling](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule)
  and look for correlated errors in the event table during the same time window.
