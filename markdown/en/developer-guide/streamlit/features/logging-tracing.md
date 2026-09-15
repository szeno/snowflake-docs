# Logging and tracing for Streamlit in Snowflake

Streamlit in Snowflake supports logging for both warehouse and container runtimes. Warehouse runtimes use the
Snowflake telemetry framework to capture log messages and trace events into an event table.
Container runtimes capture logs that your app emits to standard output and standard error,
store them in the account’s event table, and provide both live console logs and historical
log views in Snowsight.

Both runtimes store logs in the account-level event table. An account administrator must
set up and configure this event table before logs can be captured. For instructions, see
[Event table overview](/developer-guide/logging-tracing/event-table-setting-up).

- To find the event table configured for your account, run:

  Copy code

  ```
  SHOW PARAMETERS LIKE 'event_table' IN ACCOUNT;
  ```

The following table compares logging and tracing support by runtime:

| Feature | Warehouse runtime | Container runtime |
| --- | --- | --- |
| Event table logging | Supported | Supported |
| Tracing | Supported | Not supported |
| Live console logs in Snowsight | Not supported | Supported |
| Historical logs in Snowsight | Not supported | Supported |

Expand

Show lessSee more

## Container runtime logging

Feature — Generally Available

Not supported in government regions.

Container-runtime Streamlit apps run inside a Snowpark Container Services container. Snowflake automatically
captures anything your app emits to standard output and standard error and stores it in
the account’s event table. You can view these logs in Snowsight or query them
with SQL.

### Python’s logging module

Use Python’s built-in `logging` module to emit log messages from your app. The following
example configures a logger that writes INFO-level and higher messages to standard output:

Copy code

```
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)

LOGGER = logging.getLogger("my_app")
```

In order from least to most severe, Python has the following logging levels:

- DEBUG
- INFO
- WARNING
- ERROR

Setting the level to INFO captures INFO, WARNING, and ERROR messages but not DEBUG messages.

Note

By default, Python’s `logging` module writes to standard error (`sys.stderr`).
Snowflake captures both standard output and standard error, so your logs are captured
regardless of the stream you use. Setting the stream to `sys.stdout` is optional but
recommended because standard error is conventionally reserved for error output.

After configuring the logger, you can use it to log messages throughout your app code.
It is common to define a logger in a separate module and then import it into your app code:

Copy code

```
source_directory/
├── my_logger.py
├── pyproject.toml
└── streamlit_app.py
```

Copy code

```
import streamlit as st
from my_logger import LOGGER

LOGGER.info("Home page loaded")
st.title("My App")

if st.button("Run analysis"):
    LOGGER.info("Analysis button clicked")
    try:
        result = run_analysis()
        LOGGER.info("Analysis completed successfully")
    except Exception as e:
        LOGGER.error("Analysis failed: %s", e)
        st.error("Analysis failed: %s", e)
```

### Live logs in Snowsight

When you edit a container-runtime app in Snowsight, a logs pane appears below
the editor. This pane streams log messages in real time as your app emits them. A short
history of the most recent logs is displayed when you first connect.

Each log entry shows the following information:

| Column | Description |
| --- | --- |
| `Source` | `APP` for logs from your Streamlit process and user-configured loggers, or `MANAGER` for logs from the system process that manages the container. |
| `Level` | The severity level of the log message (DEBUG, INFO, WARNING, ERROR). |
| `Message` | The log message content. |

Expand

Show lessSee more

### Available live-log actions

In the upper-right corner of the logs pane, you can search and filter the logs to help you find the
information you need. This includes text search, filtering by source, and filtering by severity level.
In the three-dot menu, you can download the current logs, navigate to the historical logs, or clear the
live-logging pane. When you clear the pane, the current logs are deleted from your current view but not
from the event table. Immediately reloading the page restores the most recent logs.

### Understanding log sources

Logs from container-runtime apps have one of two sources:

- `MANAGER`: The system process inside the container that prepares and runs your app.
  Manager logs include messages about downloading your app files from the stage,
  installing Python dependencies, and starting the Streamlit server process. If you
  update your app’s dependency files while the app is running, the manager process
  reinstalls dependencies and produces additional manager logs.
- `APP`: Logs from the running Streamlit server process. This includes messages from
  your user-configured Python loggers, Streamlit’s built-in logger, and any other output
  your app writes to standard output or standard error.

The boundary between sources is the `streamlit run` command. Everything the container does
before starting the Streamlit process produces `MANAGER` logs. After the Streamlit process
starts, output from that process produces `APP` logs.

### View historical logs in Snowsight

The following steps only apply to container-runtime apps. Warehouse runtime apps
don’t have a logs pane.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**, and then select your app.
3. In the upper-right corner of the page, select **Edit**.
4. In the upper-right corner of the logs pane, select the three-dot menu (**Other actions**) » **Historical logs**.

This opens the Snowpark Container Services monitoring page for the service that runs behind your app. The logs
table shows the following columns:

| Column | Description |
| --- | --- |
| Timestamp | The timestamp of the log message. |
| Instance ID | The identifier for the container instance. This is always `0` for Streamlit apps. |
| Container | The identifier for the container instance. |
| Stream | Whether the log was emitted to standard output (`stdout`) or standard error (`stderr`). |
| Value | The JSON-formatted log message that includes `"level"`, `"message"`, `"source"`, and `"timestamp"` fields. |

Expand

Show lessSee more

For more information about the monitoring page, see
[Snowpark Container Services: Monitoring Services](/developer-guide/snowpark-container-services/monitoring-services).

### Query logs with SQL

You can query the event table directly to analyze your container-runtime app’s logs.
The following query retrieves logs from a specific Streamlit app:

Copy code

```
SELECT
    TIMESTAMP,
    RECORD['severity_text']::VARCHAR AS level,
    VALUE::VARCHAR AS message,
    RESOURCE_ATTRIBUTES['snow.database.name']::VARCHAR AS database_name,
    RESOURCE_ATTRIBUTES['snow.schema.name']::VARCHAR AS schema_name,
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS app_name,
    RECORD_ATTRIBUTES['log.iostream']::VARCHAR AS stream
FROM <event_table>
WHERE RESOURCE_ATTRIBUTES['snow.database.name'] = '<database_name>'
  AND RESOURCE_ATTRIBUTES['snow.schema.name'] = '<schema_name>'
  AND RESOURCE_ATTRIBUTES['snow.executable.name'] = '<app_name>'
  AND RECORD_TYPE = 'LOG'
  AND TIMESTAMP > DATEADD(hour, -1, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC
LIMIT 100;
```

Replace `<event_table>` with the event table name returned by the SHOW PARAMETERS command,
and replace `<database_name>`, `<schema_name>`, and `<app_name>` with the values for
your Streamlit app.

Tip

Include a TIMESTAMP filter in your event table queries to improve performance.
Event tables can contain a large volume of data from various Snowflake components.

For more information about the event table columns, see
[Event table columns](/developer-guide/logging-tracing/event-table-columns).

## Warehouse runtime logging

For Streamlit apps using warehouse runtimes, you can capture log messages and trace
events of your Streamlit app code as it runs and then analyze the results with SQL,
for example, to analyze errors. For more information, see [Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview).

Warehouse runtimes require log and trace levels to be set on the database containing your app:

Copy code

```
-- Set the log level for the database containing your app
ALTER DATABASE <database_name> SET LOG_LEVEL = INFO;

-- Set the trace level for the database containing your app
ALTER DATABASE <database_name> SET TRACE_LEVEL = ON_EVENT;
```

### Example: Logging from a warehouse-runtime app

Copy code

```
import logging
import streamlit as st

logger = logging.getLogger("simple_logger")

# Write directly to the app
st.title("Simple Logging Example")

# Get the current credentials
session = st.connection('snowflake').session()

def get_log_messages_query() -> str:
    return """
            SELECT
                TIMESTAMP,
                RECORD:"severity_text"::VARCHAR AS SEVERITY,
                RESOURCE_ATTRIBUTES:"db.user"::VARCHAR AS USER,
                VALUE::VARCHAR AS VALUE
            FROM
                SAMPLE_EVENTS
            WHERE
                SCOPE:"name" = 'simple_logger'
            ORDER BY
                TIMESTAMP DESC;
            """

button = st.button("Log a message")

if button:
    try:
        logger.info("Logging an info message through Streamlit App.")
        st.success('Logged a message')
    except Exception as e:
        logger.error("Logging an error message through Streamlit App: %s",e)
        st.error('Logged an error')

sql = get_log_messages_query()

df = session.sql(sql).to_pandas()

with st.expander("**Show All Messages**"):
     st.dataframe(df, use_container_width=True)
```

## Tracing (warehouse runtimes only)

Tracing is supported for warehouse runtimes only. You can emit trace events from your
Streamlit app and then query the event table to analyze them.

Note

The following example requires installing the `snowflake-telemetry-python` package.
For more information, see [Adding support for the telemetry package](/developer-guide/logging-tracing/tracing-python#label-tracing-events-python-telemetry-api).

Copy code

```
import streamlit as st
import time
import random
from snowflake import telemetry

def sleep_function() -> int:
    random_time = random.randint(1, 10)
    time.sleep(random_time)
    return random_time

def get_trace_messages_query() -> str:
    return """
            SELECT
                TIMESTAMP,
                RESOURCE_ATTRIBUTES :"db.user" :: VARCHAR AS USER,
                RECORD_TYPE,
                RECORD_ATTRIBUTES
            FROM
                SAMPLE_EVENTS
            WHERE
                RECORD :"name" :: VARCHAR = 'tracing_some_data'
                OR RECORD_ATTRIBUTES :"logging_demo.tracing" :: VARCHAR = 'begin_span'
            ORDER BY
                TIMESTAMP DESC;
            """

def trace_message() -> None:
    execution_time = sleep_function()
    telemetry.set_span_attribute("logging_demo.tracing", "begin_span")
    telemetry.add_event(
        "tracing_some_data",
        {"function_name": "sleep_function", "execution_time": execution_time},
    )

# Write directly to the app
st.title("Simple Tracing Example")

# Get the current credentials
session = st.connection('snowflake').session()

button = st.button("Add trace event")

if button:
    with st.spinner("Executing function..."):
        trace_message()
        st.toast("Successfully log a trace message!", icon="✅")

sql = get_trace_messages_query()

df = session.sql(sql).to_pandas()

with st.expander("**Show All Trace Messages**"):
     st.dataframe(df, use_container_width=True)
```
