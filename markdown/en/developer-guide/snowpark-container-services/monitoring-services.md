# Snowpark Container Services: Monitoring Services

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Snowflake provides a variety of mechanisms for monitoring services, jobs, and compute pools. The following sections describe the details.

A user needs the appropriate privileges on services, jobs, and compute pools to access the monitoring data. For more information, see [Privileges needed to perform operations on the service](/developer-guide/snowpark-container-services/working-with-services#label-spcs-privileges-to-perform-operations-on-services) and [Compute pool privileges](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-privileges).

## Publishing and accessing container logs

Snowflake automatically collects and stores container logs — whatever your application container emits to standard
output and standard error — to an event table for later analysis, unless you choose to opt out.
Ensure that your code outputs useful information that can help with debugging your service or conducting retrospective analysis
of your services and jobs.

Use a combination of the following settings to control which container logs are sent to the event table:

- In the service specification, use the [logExporter](/developer-guide/snowpark-container-services/specification-reference#label-snowpark-containers-spec-reference-spec-logexporters) field
  to indicate which stream (stdout/stderr) should be sent to the event table.
- In [CREATE SERVICE](/sql-reference/sql/create-service) or
  [ALTER SERVICE](/sql-reference/sql/alter-service) command, specify the LOG\_LEVEL parameter to indicate the severity at which logs are collected.

When a service container is running, you can also retrieve the container log, without saving the logs to the event table by using the
[SYSTEM$GET\_SERVICE\_LOGS](/sql-reference/functions/system_get_service_logs) system function. This process is most useful during development and testing
of your service code.

### Publishing container logs

Your application containers can publish structured or unstructured logs. When a message is emitted to standard output/standard error,
Snowflake will try to interpret it as JSON with `body` key and fall back to unstructured logs if JSON parsing fails or the key is
not found.

- **Unstructured logs:** Text that can’t be parsed as JSON
  that your application containers emit
  to standard output and standard error. Snowflake persists these strings to the value
  column in the event table.
- **Structured logs:** These are JSON text that application containers emit to standard
  output and standard error. Snowflake extracts JSON fields and saves them to specific
  columns in the event table. Then, you can query the event table and apply filters
  when exploring events.

  The following JSON structure shows supported fields that Snowflake stores in event
  table columns. If your application emits JSON that includes unsupported fields,
  as shown in the following example, Snowflake ignores those fields.

  Copy code

  ```
  {
    "severity_text": "DEBUG",    # "<DEBUG, INFO, WARN, ERROR, FATAL>",
    "body": "hello from SPCS",   # <body text>",
    "attributes": {
   "attr_key1": "attr_value1",
   "attr_key2": { "nested_key2": "nested_value2" } },
    },
    "scope": { "name": "val1" },
    "timestamp": "2025-01-01T12:34:56.789Z", # Format: RFC 3339
    # Unsupported fields are dropped.
    "another_field_key1": "another_field_val1",
    "another_field_key2": "another_field_val2",
  }
  ```

  The following table shows the JSON-log field names and the corresponding event-table
  column names where Snowflake stores their values. For description of the log fields,
  see the
  [Event table columns](/developer-guide/logging-tracing/event-table-columns) descriptions.

  | JSON field | Event table column | Comment |
  | --- | --- | --- |
  | severity\_text | [RECORD](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column) | Snowflake saves both `severity_text` and the Snowflake-assigned `severity_number` as Object fields in this column. |
  | attributes | [RECORD\_ATTRIBUTES](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-attributes-column). | The fields from structured log are copied as Object fields in this column. |
  | scope | [SCOPE](/developer-guide/logging-tracing/event-table-columns#label-event-table-scope-column) | The fields from the structured log are copied as Object fields in this column. |
  | timestamp | [TIMESTAMP](/developer-guide/logging-tracing/event-table-columns#label-event-table-timestamp-column) |  |

  Expand

  Show lessSee more

  The following example shows a container log stored in an event table:

  ```
  +----------------------+--------------------------+-------------+----------------------------+-------------------+---------------------------------------------------------------------------------------------------+
  |        VALUE         |       TIMESTAMP          | RECORD_TYPE |           RECORD           |       SCOPE       |            RECORD_ATTRIBUTES           |                   RESOURCE_ATTRIBUTES                    |
  +----------------------+--------------------------+-------------+----------------------------+-------------------+---------------------------------------------------------------------------------------------------+
  | "hello from SPCS"    | 2025-01-01T12:34:56.789Z | LOG         | {                          | {                 | {                                      | {                                                        |
  |                      |                          |             |   "severity_number": 5,    |   "name1": "val1" |   "attr_key1": "attr_value1",          |   "snow.account.name": "****",                           |
  |                      |                          |             |   "severity_text": "DEBUG" | }                 |   "attr_key2": {                       |   "snow.compute_pool.id": "****",                        |
  |                      |                          |             | }                          |                   |     "nested_key2": "nested_value2"     |   "snow.compute_pool.name": "MYPO****",                  |
  |                      |                          |             |                            |                   |   }                                    |   "snow.compute_pool.node.id": "****",                   |
  |                      |                          |             |                            |                   | }                                      |   "snow.compute_pool.node.instance_family": "CPU_****",  |
  |                      |                          |             |                            |                   |                                        |   "snow.database.id": "****",                            |
  |                      |                          |             |                            |                   |                                        |   "snow.database.name": "MYDB****",                      |
  |                      |                          |             |                            |                   |                                        |   "snow.query.id": "****",                               |
  |                      |                          |             |                            |                   |                                        |   "snow.schema.id": "****",                              |
  |                      |                          |             |                            |                   |                                        |   "snow.schema.name": "MYSC****",                        |
  |                      |                          |             |                            |                   |                                        |   "snow.service.container.name": "main****",             |
  |                      |                          |             |                            |                   |                                        |   "snow.service.container.run.id": "****",               |
  |                      |                          |             |                            |                   |                                        |   "snow.service.id": "****",                             |
  |                      |                          |             |                            |                   |                                        |   "snow.service.instance": "0",                          |
  |                      |                          |             |                            |                   |                                        |   "snow.service.name": "TEST****",                       |
  |                      |                          |             |                            |                   |                                        |   "snow.service.type": "Service"                         |
  |                      |                          |             |                            |                   |                                        | }                                                        |
  +----------------------+--------------------------+-------------+----------------------------+-------------------+----------------------------------------+----------------------------------------------------------+
  ```

  If you use Python for your application code, you can use
  the [Snowflake-provided log formatter](https://pypi.org/project/snowflake-telemetry-python/)
  (`SnowflakeLogFormatter`) to emit structured logs, as shown in the following example:

  Copy code

  ```
  from snowflake.telemetry.logs import SnowflakeLogFormatter

  handler = logging.StreamHandler(stream=get_stream(arguments.stream))
  handler.setFormatter(SnowflakeLogFormatter())
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG) # info by default

  # Emit logs with record attributes (`extra` argument)
  logger.warning("warning log record with attributes", extra={"custom": True})
  logger.debug("debug log with nested attributes", extra={"nested": {"key1": [1, 2, 3]}})
  ```

### Accessing container logs

You can currently access container logs by using the following options:

- **Use the service helper method:** We recommend calling the
  [Using the <service-name>!SPCS\_GET\_LOGS function](#label-spcs-monitoring-services-using-spcs-get-logs) to retrieve container logs of the specified service or job, collected by Snowflake in the event table.
- **Use the event table directly:** If you have full access to the event table, you can query the event table directly to get historical logs.
- **Use the SYSTEM$GET\_SERVICE\_LOGS system function:** [Call SYSTEM$GET\_SERVICE\_LOGS](#label-spcs-working-monitoring-services-get-service-logs) to retrieve the logs of the currently running service or job container.

### Using the <service-name>!SPCS\_GET\_LOGS function

The [<service\_name>!SPCS\_GET\_LOGS](/sql-reference/functions/spcs_get_logs) table function returns logs from the containers of the specified job. These logs are collected by Snowflake and are stored in the event table.

The following list explains the advantages of using this table function:

- You can retrieve logs for a specific service.
- You can retrieve logs within a specified time range.
- The caller needs either the service owner role or a role with the MONITOR privilege on the service. The caller does not need access to the entire event table,
  which can be beneficial for customers with strict information-security requirements.

For `service_name`, you specify the name of the service. The function returns logs Snowflake collected from containers of that service (see [Publishing and accessing container logs](#label-snowpark-containers-working-with-services-local-logs)).

You can optionally specify a date range. By default, the function returns one-day logs. For example, the query retrieved logs that Snowflake collected from containers of the `my_test_job` job over the past day, which is the default.

> Copy code
>
> ```
> SELECT * FROM TABLE(mydb.myschema.my_test_job!SPCS_GET_LOGS());
> ```
>
> Example output:
>
> ```
> +-------------------------+-------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------+
> | TIMESTAMP               | INSTANCE_ID | CONTAINER_NAME | LOG                                                                                                                                                                 | RECORD_ATTRIBUTES          |
> |-------------------------+-------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------|
> | 2025-06-26 00:23:40.281 |           0 | main           | job-tutorial - INFO - Job finished                                                                                                                                  | {                          |
> |                         |             |                |                                                                                                                                                                     |   "log.iostream": "stdout" |
> |                         |             |                |                                                                                                                                                                     | }                          |
> | 2025-06-26 00:23:38.787 |           0 | main           | job-tutorial - INFO - Executing query [select current_time() as time,'hello'] and writing result to table [results]                                                 | {                          |
> |                         |             |                |                                                                                                                                                                     |   "log.iostream": "stdout" |
> |                         |             |                |                                                                                                                                                                     | }                          |
> | 2025-06-26 00:23:38.787 |           0 | main           | job-tutorial - INFO - Connection succeeded. Current session context: database="TUTORIAL_DB", schema="DATA_SCHEMA", warehouse="TUTORIAL_WAREHOUSE", role="TEST_ROLE" | {                          |
> |                         |             |                |                                                                                                                                                                     |   "log.iostream": "stdout" |
> |                         |             |                |                                                                                                                                                                     | }                          |
> | 2025-06-26 00:23:36.852 |           0 | main           | job-tutorial - INFO - Job started                                                                                                                                   | {                          |
> |                         |             |                |                                                                                                                                                                     |   "log.iostream": "stdout" |
> |                         |             |                |                                                                                                                                                                     | }                          |
> +-------------------------+-------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------+
> ```

For more information about calling this method, see [<service\_name>!SPCS\_GET\_LOGS](/sql-reference/functions/spcs_get_logs).

### Using event table

Snowflake can capture logs sent from containers to the standard output and standard error streams into the event table configured for your account.
For more information about configuring an event table, see
[Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview).

You control which streams are collected (all, standard error only, or none) that you want stored in an event table by using the
[spec.logExporters field](/developer-guide/snowpark-container-services/specification-reference#label-snowpark-containers-spec-reference-spec-logexporters) in the service specification file.

You can then query the event table for events. To find the active event table for the account, use the [SHOW PARAMETERS](/sql-reference/sql/show-parameters) command to check the value of the [EVENT\_TABLE](/sql-reference/parameters#label-event-table) parameter:

Copy code

```
SHOW PARAMETERS LIKE 'event_table' IN ACCOUNT;
```

The parameter specifies the active event table for the account.

Next, query that event table. The following SELECT statement retrieves Snowflake service and job events recorded in the past hour:

Copy code

```
SELECT TIMESTAMP, RESOURCE_ATTRIBUTES, RECORD_ATTRIBUTES, VALUE
FROM <current_event_table_for_your_account>
WHERE timestamp > dateadd(hour, -1, current_timestamp())
AND RESOURCE_ATTRIBUTES:"snow.service.name" = '<service_name>'
AND RECORD_TYPE = 'LOG'
ORDER BY timestamp DESC
LIMIT 10;
```

Snowflake recommends that you include a timestamp in the WHERE clause of event
table queries, as shown in this example. This is particularly important
because of the potential volume of data generated by various Snowflake
components. By applying filters, you can retrieve a smaller subset
of data, which improves query performance.

The event table includes the following columns, which provide useful information regarding the logs collected
by Snowflake from your container:

- **TIMESTAMP:** Shows when Snowflake collected the log.
- **RESOURCE\_ATTRIBUTES:** Provides a JSON object that identifies the Snowflake service and the container in the service that generated
  the log message. For example, it furnishes details such as the service name, container name, and compute pool name that were specified
  when the service was run.

  Copy code

  ```
  {
    "snow.account.name": "SPCSDOCS1",
    "snow.compute_pool.id": 20,
    "snow.compute_pool.name": "TUTORIAL_COMPUTE_POOL",
    "snow.compute_pool.node.id": "a17e8157",
    "snow.compute_pool.node.instance_family": "CPU_X64_XS",
    "snow.database.id": 26,
    "snow.database.name": "TUTORIAL_DB",
    "snow.schema.id": 212,
    "snow.schema.name": "DATA_SCHEMA",
    "snow.container.instance": "0",
    "snow.service.container.name": "echo",
    "snow.service.container.run.id": "b30566",
  "snow.service.id": 114,
    "snow.service.name": "ECHO_SERVICE2",
    "snow.service.type": "Service"
  }
  ```
- **RECORD\_ATTRIBUTES:** For a Snowflake service, it identifies an
  error source (standard output or standard error).

  Copy code

  ```
  { "log.iostream": "stdout" }
  ```
- **VALUE:** Standard output and standard error are broken into lines,
  and each line generates a record in the event table.

  ```
  "echo-service [2023-10-23 17:52:27,429] [DEBUG] Sending response: {'data': [[0, 'Joe said hello!']]}"
  ```

### Using SYSTEM$GET\_SERVICE\_LOGS

The [SYSTEM$GET\_SERVICE\_LOGS](/sql-reference/functions/system_get_service_logs) function returns logs of the currently running service container. After a container exits, you can continue to access the logs by using the system function for a short time. System functions are most useful during development and testing, when you are initially authoring a service or a job.

You provide the service name, instance ID, container name, and optionally the number of most recent log lines to retrieve. If only one service instance is running, the service instance ID is 0. For example, the following statement command retrieves the
trailing 10 lines from the log of a container named `echo`
that belongs to instance 0 of a service named `echo_service`:

Copy code

```
SELECT SYSTEM$GET_SERVICE_LOGS('echo_service', '0', 'echo', 10);
```

Example output:

```
+--------------------------------------------------------------------------+
| SYSTEM$GET_SERVICE_LOGS                                                  |
|--------------------------------------------------------------------------|
| 10.16.6.163 - - [11/Apr/2023 21:44:03] "GET /healthcheck HTTP/1.1" 200 - |
| 10.16.6.163 - - [11/Apr/2023 21:44:08] "GET /healthcheck HTTP/1.1" 200 - |
| 10.16.6.163 - - [11/Apr/2023 21:44:13] "GET /healthcheck HTTP/1.1" 200 - |
| 10.16.6.163 - - [11/Apr/2023 21:44:18] "GET /healthcheck HTTP/1.1" 200 - |
+--------------------------------------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.878s
```

If you don’t have the information about the service that you need to call the function — such as the instance ID or container name — you can first run the [SHOW SERVICE CONTAINERS IN SERVICE](/sql-reference/sql/show-service-containers-in-service) command to get information
about the service instances and containers running in each instance.

The SYSTEM$GET\_SERVICE\_LOGS function has the following limitations:

- It merges standard output and standard error streams. The function provides no indication of which stream the output came from.
- It reports the captured data for a specific container in a single
  service instance.
- It only reports logs for a running container. The function can’t fetch
  logs from a previous container that was restarted or from a
  container of a service that is stopped or deleted.
- The function returns up to 100 KB of data.

## Access platform metrics

Snowflake provides metrics for [compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool) in your account and [services](/developer-guide/snowpark-container-services/working-with-services) running on those compute pools. These metrics, provided by Snowflake, are also referred to as platform metrics.

- **Event-table service metrics:** Individual services publish metrics. These are a subset of the compute pool metrics that provide information specific to the service. The target use case for this is to observe the resource utilization of a specific service. In the service specification, you define which metrics you want Snowflake to record in the event table while the service is running.
- **Compute pool metrics:** Each compute pool also publishes metrics that provide information about what is happening inside that compute pool. The target use case for this is to observe the compute pool utilization. To access your compute pool metrics, you will need to write a service that uses Prometheus-compatible API to poll the metrics that the compute pool publishes.

### Accessing event-table service metrics

To log metrics from a service into the event table configured for your account, include the following section in your service specification:

Copy code

```
platformMonitor:
  metricConfig:
    groups:
    - <group 1>
    - <group 2>
    - ...
```

Where each `{group N}` refers to a [predefined metrics group](#label-spcs-available-platform-metrics) that you are interested in; for example, `system`, `network`, or `storage`. For more information, see the [spec.platformMonitor field](/developer-guide/snowpark-container-services/specification-reference#label-snowpark-containers-spec-reference-platform-monitor) section in the documentation on the service specification.

While the service is running, Snowflake records these metrics to the event table in your account. You can read these metrics in the following ways:

- **Using the service helper method:** The [<service\_name>!SPCS\_GET\_METRICS](/sql-reference/functions/spcs_get_metrics) table function returns metrics Snowflake collected for the specified service. The following list explains advantages of using this table function:

  - You can retrieve metrics for a specific service.
  - You can retrieve metrics within a specified time range.
  - The caller doesn’t need access to the entire events table, which can be beneficial for customers with strict information security requirements.

  The following SELECT statement uses the table function to retrieve platform events for the specified service that was recorded in the past hour:

  Copy code

  ```
  SELECT *
    FROM TABLE(mydb.myschema.echo_service!SPCS_GET_METRICS(start_time => dateadd('hour', -1, current_timestamp())));
  ```
- **Query the events table directly:** You can query your event table to read the metrics. The following query retrieves the service metrics that were recorded in the past hour for the service `my_service`:

  Copy code

  ```
  SELECT timestamp, value
    FROM my_event_table_db.my_event_table_schema.my_event_table
    WHERE timestamp > DATEADD(hour, -1, CURRENT_TIMESTAMP())
   AND RESOURCE_ATTRIBUTES:"snow.service.name" = 'MY_SERVICE'
   AND RECORD_TYPE = 'METRIC'
   ORDER BY timestamp DESC
   LIMIT 10;
  ```

  If you don’t know the name of the active event table for the account, run the [SHOW PARAMETERS](/sql-reference/sql/show-parameters) command to display the value of the account-level [EVENT\_TABLE](/sql-reference/parameters#label-event-table) parameter:

  Copy code

  ```
  SHOW PARAMETERS LIKE 'event_table' IN ACCOUNT;
  ```

  For more information about event tables, see [Using event table](#label-snowpark-containers-working-with-services-using-event-table).

**Example**

To create an example service that records metrics to the event table that is configured for your account, complete the following steps.

1. Create a service named `echo_service` by following the steps in [Tutorial 1](/developer-guide/snowpark-container-services/tutorials/tutorial-1), with one change. In step 3, where you create a service, use the following CREATE SERVICE command, which adds the `platformMonitor` field in the modified service specification:

   Copy code

   ```
   CREATE SERVICE echo_service
     IN COMPUTE POOL tutorial_compute_pool
     FROM SPECIFICATION $$
    spec:
      containers:
      - name: echo
        image: /tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest
        env:
          SERVER_PORT: 8000
          CHARACTER_NAME: Bob
        readinessProbe:
          port: 8000
          path: /healthcheck
      endpoints:
      - name: echoendpoint
        port: 8000
        public: true
      platformMonitor:
        metricConfig:
          groups:
          - system
          - system_limits
      $$
    MIN_INSTANCES=1
    MAX_INSTANCES=1;
   ```

> After the service is running, Snowflake starts recording the metrics in the specified metric groups to the event table.

1. Access the metrics by calling the <service\_name>!SPCS\_GET\_METRICS function or by querying the event table. For example, retrieve metrics reported in the last hour by the echo\_service service:
   - Use the [<service\_name>!SPCS\_GET\_METRICS](/sql-reference/functions/spcs_get_metrics) helper function:

     Copy code

     ```
     SELECT *
     FROM TABLE(mydb.myschema.echo_service!SPCS_GET_METRICS(START_TIME => DATEADD('hour', -1, CURRENT_TIMESTAMP())));
     ```
   - Query the event table directly:

     Copy code

     ```
     SELECT timestamp, value
      FROM my_events
      WHERE timestamp > DATEADD(hour, -1, CURRENT_TIMESTAMP())
        AND RESOURCE_ATTRIBUTES:"snow.service.name" = 'ECHO_SERVICE'
        AND RECORD_TYPE = 'METRIC'
        AND RECORD:metric.name = 'container.cpu.usage'
        ORDER BY timestamp DESC
        LIMIT 100;
     ```

### Access compute pool metrics

[Compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool) metrics offer insights into the nodes in the compute pool and the services running on them. Each node reports node-specific metrics, such as the amount of available memory for containers, as well as service metrics, like the memory usage by individual containers. The compute pool metrics provide information from a node’s perspective.

Each node has a metrics publisher that listens on TCP port 9001. Other services can make an HTTP GET request with the path `/metrics` to port 9001 on the node. To discover the node’s IP address, retrieve SRV records (or A records) from DNS for the `discover.monitor.compute_pool_name.cp.spcs.internal` hostname. Then, create another service in your account that actively polls each node to retrieve the metrics.

The body in the response provides the metrics using the
[Prometheus format](https://prometheus.io/docs/instrumenting/exposition_formats/#text-based-format)
as shown in the following example metrics:

```
# HELP node_memory_capacity Defines SPCS compute pool resource capacity on the node
# TYPE node_memory_capacity gauge
node_memory_capacity{snow_compute_pool_name="MY_POOL",snow_compute_pool_node_instance_family="CPU_X64_S",snow_compute_pool_node_id="10.244.3.8"} 1
node_cpu_capacity{snow_compute_pool_name="MY_POOL",snow_compute_pool_node_instance_family="CPU_X64_S",snow_compute_pool_node_id="10.244.3.8"} 7.21397383168e+09
```

Note the following:

- The response body starts with `# HELP` and `# TYPE`, which provide a short description and the type of the metric. In this example, the `node_memory_capacity` metric is of type `gauge`.
- It is then followed by the metric’s name, a list of labels describing a specific resource (data point), and its value. In this example, the metric (named `node_memory_capacity`) provides memory information, indicating that the node has 7.2 GB available memory. The metric also includes metadata in the form of labels as shown:

  ```
  snow_compute_pool_name="MY_POOL",
  snow_compute_pool_node_instance_family="CPU_X64_S",snow_compute_pool_node_id="10.244.3.8"
  ```

You can process these metrics any way you choose; for example, you might store metrics in a database and use a UI (such as a Grafana dashboard) to display the information.

Note

- Snowflake does not provide any aggregation of metrics. For example, to get metrics for a given service, you must query all nodes that are running instances of that service.
- The compute pool must have a DNS-compatible name for you to access the metrics.
- The endpoint exposed by a compute pool can be accessed by a service using a role that has the OWNERSHIP or MONITOR privilege on the compute pool.

For a list of available compute pool metrics, see [Available platform metrics](#label-spcs-available-platform-metrics).

**Example**

For an example of configuring Prometheus to poll your compute pool for metrics, see the [compute pool metrics tutorials](https://github.com/Snowflake-Labs/spcs-templates/tree/main/user-metrics).

### Available platform metrics

The following is a list of available platform metrics groups and metrics within each group. Note that *storage* metrics are currently only collected from block storage volumes.

| Metric group   Metric name | Unit | Type | resource\_attributes | record\_attributes | Description |
| --- | --- | --- | --- | --- | --- |
| system   container.cpu.usage | cpu cores | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | Average number of CPU cores used since last measurement. 1.0 indicates full utilization of 1 CPU core. Max value is number of cpu cores available to the container. |
| system   container.memory.usage | bytes | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | Memory used, in bytes. |
| system   container.gpu.memory.usage | bytes | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | Per-GPU memory used, in bytes. The source GPU is denoted in the ‘gpu’ attribute. |
| system   container.gpu.utilization | ratio | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id | gpu | Ratio of per-GPU usage to capacity. The source GPU is denoted in the ‘gpu’ attribute. |
| system\_limits   container.cpu.limit | cpu cores | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | CPU resource limit from the service specification. If no limit is defined, defaults to node capacity. |
| system\_limits   container.gpu.limit | gpus | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id | gpu | GPU count limit from the service specification. If no limit is defined, the metric is not emitted. |
| system\_limits   container.memory.limit | bytes | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | Memory limit from the service specification. If no limit is defined, defaults to node capacity. |
| system\_limits   container.cpu.requested | cpu cores | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | CPU resource request from the service specification. If no limit is defined, this defaults to a value chosen by Snowflake. |
| system\_limits   container.gpu.requested | gpus | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id | gpu | GPU count from the service specification. If no limit is defined, the metric is not emitted. |
| system\_limits   container.memory.requested | bytes | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id | gpu | Memory request from the service specification. If no limit is defined, this defaults to a value chosen by Snowflake. |
| system\_limits   container.gpu.memory.capacity | bytes | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id | gpu | Per-GPU memory capacity. The source GPU is denoted in the ‘gpu’ attribute. |
| status   container.restarts | restarts | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | Number of times Snowflake restarted the container. |
| status   container.state.finished | boolean | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | When the container is in the ‘finished’ state, this metric will be emitted with the value 1. |
| status   container.state.last.finished.reason | boolean | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id | reason | If the container has restarted previously, this metric will be emitted with the value 1. The ‘reason’ label describes why the container last finished. |
| status   container.state.last.finished.exitcode | integer | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | If a container has restarted previously, this metric will contain the exit code of the previous run. |
| status   container.state.pending | boolean | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | When a container is in the ‘pending’ state, this metric will be emitted with the value 1. |
| status   container.state.pending.reason | boolean | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id | reason | When a container is in the ‘pending’ state, this metric will be emitted with the value 1. The ‘reason’ label describes why the container was most recently in the pending state. |
| status   container.state.running | boolean | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | When a container is in the ‘running’ state, this metric will have the value 1. |
| status   container.state.started | boolean | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id |  | When a container is in the ‘started’ state, this metric will have the value 1. |
| network   network.egress.denied.packets | packets | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id |  | Network egress total denied packets from service instance due to policy validation failures. |
| network   network.egress.received.bytes | bytes | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id |  | Network egress total bytes received by service instance from remote destinations. |
| network   network.egress.received.packets | packets | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id |  | Network egress total packets received by service instance from remote destinations. |
| network   network.egress.transmitted.bytes | byte | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id |  | Network egress total bytes transmitted by service instance out to remote destinations. |
| network   network.egress.transmitted.packets | packets | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id |  | Network egress total packets transmitted by service instance out to remote destinations. |
| network   network.ingress.connections.active | connections | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id snow.endpoint.name |  | Number of active ingress connections for this endpoint. This metric includes the resource attribute `snow.endpoint.name` to determine the value per endpoint. |
| network   network.ingress.cps | connections/sec | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.service.container.name snow.query.id snow.endpoint.name |  | Number of ingress connections to this endpoint per second. This metric includes the resource attribute `snow.endpoint.name` to help you to determine the value per endpoint. |
| storage   volume.capacity | bytes | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id | snow\_volume\_id snow\_volume\_name snow\_volume\_replica volume\_type | Size of the filesystem. The target volume is denoted in the `volume_name` attribute. |
| storage   volume.io.inflight | operations | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id | snow\_volume\_id snow\_volume\_name snow\_volume\_replica volume\_type | Number of active filesystem I/O operations at current instant. The target volume is denoted in the `volume_name` attribute. |
| storage   volume.read.throughput | bytes/sec | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id | snow\_volume\_id snow\_volume\_name snow\_volume\_replica volume\_type | Filesystem reads throughput in bytes per second since last measurement. The target volume is denoted in the `volume_name` attribute. |
| storage   volume.read.iops | operations/sec | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id | snow\_volume\_id snow\_volume\_name snow\_volume\_replica volume\_type | Filesystem read operations per second since last measurement. The target volume is denoted in the `volume_name` attribute |
| storage   volume.usage | bytes | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id | snow\_volume\_id snow\_volume\_name snow\_volume\_replica volume\_type | Total number of bytes used in the filesystem since last measurement. The target volume is denoted in the `volume_name` attribute. |
| storage   volume.write.throughput | bytes/sec | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id | snow\_volume\_id snow\_volume\_name snow\_volume\_replica volume\_type | Filesystem write throughput in bytes per second since last measurement. The target volume is denoted in the `volume_name` attribute. |
| storage   volume.write.iops | operations/sec | gauge | snow.account.name snow.compute\_pool.id snow.compute\_pool.name snow.compute\_pool.node.id snow.compute\_pool.node.instance\_family snow.database.id snow.database.name snow.schema.id snow.schema.name snow.service.id snow.service.name snow.service.type snow.container.instance snow.query.id | snow\_volume\_id snow\_volume\_name snow\_volume\_replica volume\_type | Filesystem write operations per second since last measurement. The target volume is denoted in the `volume_name` attribute. |

Expand

Show lessSee more

As shown in the preceding table, the platform metrics contain the following attributes. These attributes are stored in the event table resource\_attributes and record\_attributes columns. Snowflake exposes these attributes as Prometheus labels when scraped directly from the node.

**Resource attributes**

- `snow.account.name`: Name of the account that launched the service.
- `snow.compute_pool.id`: Id of the compute pool where the service was scheduled.
- `snow.compute_pool.name`: Name of the compute pool where service was scheduled.
- `snow.compute_pool.node_id`: Id of the compute pool node running the container that produced this metric.
- `snow.compute_pool.node.instance_family`: The type of the instance family of the compute pool that is running the service. For more information, see [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool).
- `snow.database.id`: Id of the database that owns the service.
- `snow.database.name`: Name of the database that owns the service.
- `snow.schema.id`: Id of the schema that owns the service.
- `snow.schema.name`: Name of the schema that owns the service
- `snow.service.id`: Id of the service.
- `snow.service.name`: Name of the service.
- `snow.service.type`: Specifies whether the container is a job service or a long-running service.
- `snow.service_container.instance`: Id of the container instance that produced the metric.
- `snow.service.container.name`: Name of the container that produced the metric.
- `snow.query.id`: The [uuid of the query](/sql-reference/functions/last_query_id) that created the service.

**Record attributes**

- `gpu`: Index of the gpu from which this metric originated, starting with 0.
- `reason`: Explains the container state. This attribute appears only for metrics that end with reason suffix.

  - `spcs.container.state.pending.reason`

    - `FailedToPullImage`: Container cannot pull image.
    - `FailingToStartContainer`: Container cannot be started. It is getting scheduled to the node, but then fails.
    - `ServiceRunError`: Runtime error occurred resulting in the container eviction.
    - `ServiceSpecError`: Container cannot be scheduled because error in service specification.
    - `ServiceCreateError`: Error during container initialization.
    - `Initializing`: Container is currently initializing.
    - `Creating`: Container in process of creating, for example, pulling an image.
  - `container.state.last.finished.reason`

    - `Done`: Container finished without error.
    - `Failed`: Container terminated with an error.
    - `FailedWithOOM`: Container terminated after exceeding memory limit from service specification.
    - `FailedToStart`: Container did not start due to error.
- `resource`: Node resource that the metric describes (cpu, memory, gpu, gpu\_memory).
- `snow_volume_id`: Id of the volume.
- `snow_volume_name`: Name of the volume.
- `snow_volume_replica`: Indicates the service instance’s ordinal identity within a service. For example, `snow_volume_replica="3"` represents the third instance of that service.
- `volume_type`: Volume type (local, memory, block, and Snowflake stage).

## Publishing and accessing application metrics

Application metrics and traces are generated by your service in contrast to platform metrics that Snowflake generates. Your service
containers can generate OLTP or Prometheus metrics and Snowflake publishes them to the event table configured for your account.

Note that you should ensure that your service container code outputs metrics with the correct units, aggregation, and instrumentation
types to generate metrics that are meaningful and effective for your analysis.

### Publishing OTLP application metrics and traces

Snowflake runs an OTel collector that your service container can use to publish OTLP application metrics and traces. That is, a service container can push metrics to the OTel collector endpoints, which Snowflake then writes to the event table configured for your Snowflake account along with the originating service details.

It works as follows:

- Snowflake automatically populates the following environment variables in your service container that provide the OTel collector endpoints where containers can publish application metrics and traces:

  - `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`
  - `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`
- The [standard OTLP client](https://opentelemetry.io/docs/languages/) looks for these environment variables to discover the OTel collector automatically. This enables your service container to publish metrics and traces using this client.

#### Configuring OTLP application Trace IDs

Traces must use the Snowflake Trace ID format to be viewable in [Snowflake Trail](https://www.snowflake.com/en/product/features/snowflake-trail/) and allow for performant lookup.

Snowflake provides Python and Java libraries to simplify Trace ID generator setup. The following examples show how to override the default OpenTelemetry trace ID generator with these libraries.

Copy code

```
from opentelemetry.sdk.trace import TracerProvider
from snowflake.telemetry.trace import SnowflakeTraceIdGenerator

trace_id_generator = SnowflakeTraceIdGenerator()
tracer_provider = TracerProvider(
    resource=Resource.create({"service.name": SERVICE_NAME}),
    id_generator=trace_id_generator
)
```

For more information, see [snowflake-telemetry-python](https://pypi.org/project/snowflake-telemetry-python/) on PyPI.

Copy code

```
import io.opentelemetry.sdk.autoconfigure.AutoConfiguredOpenTelemetrySdk;
import com.snowflake.telemetry.trace.SnowflakeTraceIdGenerator;

static OpenTelemetry initOpenTelemetry() {
  return AutoConfiguredOpenTelemetrySdk.builder()
      .addPropertiesSupplier(
          () ->
              Map.of(...config options...)
      .addTracerProviderCustomizer(
          (tracerProviderBuilder, configProperties) -> {
            tracerProviderBuilder.setIdGenerator(SnowflakeTraceIdGenerator.INSTANCE);
            return tracerProviderBuilder;
          })
      .build()
      .getOpenTelemetrySdk();
```

For more information about installing `com.snowflake.telemetry`, see [Setting up your Java and Scala environment to use the Telemetry class](/developer-guide/logging-tracing/telemetry-build-maven).

A trace ID generator can be implemented for any other programming language as well. The 16-byte ID (big endian) must contain a timestamp in the four highest-order bytes. The other bytes should contain random bits. For more information, see [Python reference implementation](https://github.com/snowflakedb/snowflake-telemetry-python/blob/0c5b4faf024997d993f7cd1d00e6ae0cb0bb7d08/src/snowflake/telemetry/trace/__init__.py#L14).

### Publishing Prometheus application metrics

Snowflake supports Prometheus metrics where instead of pushing OTLP metrics, your application might expose Prometheus metrics to be polled
by a Snowflake-provided collector. For Snowflake to collect these application metrics from your service and publish them to the event
table, follow these steps:

- Have your service listen on a port, which exposes your Prometheus metrics.
- Include in your service a Snowflake-provided container (also referred to as “sidecar” container), with necessary configuration to pull
  the metrics from your service container.

The Prometheus sidecar pulls the application metrics from the container at a scheduled frequency, converts the Prometheus format to OTLP format, and pushes the metrics to the OTel collector. The OTel collector then publishes those metrics into the event table configured for your Snowflake account.

Note

Snowflake doesn’t support Prometheus Summary [metric type](https://prometheus.io/docs/concepts/metric_types/), as it is [deprecated by OpenTelemetry](https://opentelemetry.io/docs/specs/otel/metrics/data-model/#summary-legacy). Use the Histogram type instead.

You add the Prometheus sidecar container to the service specification as another container and include an argument to specify the HTTP endpoint exposed by your container, using the following format:

```
localhost:{PORT}/{METRICS_PATH}, {SCRAPE_FREQUENCY}
```

It specifies a port number, path, and frequency at which the sidecar should pull the metrics.

An example service specification fragment shows the sidecar container scraping metrics every minute from your service container from port 8000 and pulling metrics from the path “/metrics”:

Copy code

```
spec:
  containers:
  - name: <name>
    image: <image-name>
    .....
  - name: prometheus
    image: /snowflake/images/snowflake_images/monitoring-prometheus-sidecar:0.0.1
    args:
      - "-e"
      - "localhost:8000/metrics,1m"
```

In the specification:

- `image` is the Snowflake-provided sidecar container image.
- `args` provides necessary configuration for the prometheus container to scrape metrics:

  - From port 8000 provided by your container. The port is required in this prometheus container configuration.
  - Using path “/metrics”. It is optional. If not specified, “/metrics” is the default path.
  - Every minute. It is optional. If not specified, “1m” is the default.

  If you leverage the defaults, this is the equivalent configuration for scraping metrics:

  Copy code

  ```
  spec:
   ...
   args:
     - "-e"
     - "localhost:8000"
  ```

Note

The Prometheus sidecar container is only supported for services (not jobs). If you want to collect application metrics for a job, it must push the metrics to the OTel collector.

### Accessing application metrics and traces in the event table

You can query the event table to retrieve application metrics. The following query retrieves the application metrics collected in the past hour.

Copy code

```
SELECT timestamp, record:metric.name, value
  FROM <current_event_table_for_your_account>
  WHERE timestamp > dateadd(hour, -1, CURRENT_TIMESTAMP())
    AND resource_attributes:"snow.service.name" = <service_name>
    AND scope:"name" != 'snow.spcs.platform'
    AND record_type = 'METRIC'
  ORDER BY timestamp DESC
  LIMIT 10;
```

For more information about event tables, see [Event table overview](/developer-guide/logging-tracing/event-table-setting-up). You can visualize these metrics in [Snowflake dashboards](/user-guide/ui-snowsight-dashboards).

You can also query your event table to view the application traces. For example, to retrieve application traces from the past hour, in the preceding query, replace the `record_type` condition as follows:

Copy code

```
AND record_type = 'SPAN' OR record_type = 'SPAN_EVENT'
```

Traces can be visualized in the [Snowflake trail](https://www.snowflake.com/en/data-cloud/snowflake-trail/) viewer.

Metrics and traces contain both user-defined and Snowflake-defined attributes as resource and record attributes. Note that the `snow.` prefix is reserved for Snowflake-generated attributes, Snowflake ignores custom attributes that use this prefix. To see a list of Snowflake defined attributes see [Available platform metrics](#label-spcs-available-platform-metrics).

[Example code](https://github.com/Snowflake-Labs/spcs-templates/tree/main/application-observability) is provided in both Python and Java that demonstrates instrumenting an application with custom metrics and traces using the OTLP SDK. The examples show how to configure Snowflake Trace ID generation for compatibility with the Snowflake trail viewer for traces.

## Accessing platform events

Snowflake records events that provide visibility into the status and history of services. These Snowflake-provided events are referred to as *platform events*.

For example, if your service container is currently running but was restarted a day earlier due to a fatal error (such as an out-of-memory condition), you can use platform events to view this historical event.

Snowflake logs these platform events in the [event table](#label-snowpark-containers-working-with-services-using-event-table) in your account. By default, platform events are not logged. To enable the logging of platform events, set the [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) parameter when creating resources (for example, when running CREATE SERVICE) or use ALTER statements to update the level for existing resources.

Container log lines from standard output and standard error still use [LOG\_LEVEL](/sql-reference/parameters#label-log-level); platform events use `LOG_EVENT_LEVEL`. For more information, see [Parameters](/sql-reference/parameters) and [New LOG\_EVENT\_LEVEL parameter to control events](/release-notes/bcr-bundles/2026_02/bcr-2229).

Note

If the LOG\_EVENT\_LEVEL parameter is not set at the resource level, Snowflake can inherit the value of the parameter that is set at a higher level. For a service, Snowflake can inherit the value of the LOG\_EVENT\_LEVEL parameter that is set on the schema, database, or the account of the service. For more information, see [How Snowflake determines the level in effect](/developer-guide/logging-tracing/telemetry-levels#label-telemetry-level-effective).

You can check the current value set for a service by running [SHOW PARAMETERS … IN SERVICE](/sql-reference/sql/show-parameters):

Copy code

```
SHOW PARAMETERS LIKE 'LOG_EVENT_LEVEL' IN SERVICE mydb.myschema.myservice;
```

The value of the LOG\_EVENT\_LEVEL parameter determines the severity of platform events you want recorded in the event table. In the current implementation, the supported LOG\_EVENT\_LEVEL values are: `INFO` and `ERROR`.

- If you want to record only ERROR platform events in the event table, set LOG\_EVENT\_LEVEL to `ERROR`.
- If you want `INFO` and `ERROR` platform events recorded in the event table, set LOG\_EVENT\_LEVEL to `INFO`.
- If you want to stop recording platform events in the event table, set LOG\_EVENT\_LEVEL to `OFF`.

For more information, see [Setting telemetry levels](/developer-guide/logging-tracing/telemetry-levels#label-telemetry-level-setting).

### Query platform events

After you configure LOG\_EVENT\_LEVEL for your resource, Snowflake records the platform events to the active event table in your Snowflake account. You can access these events in the following ways:

- **Using the service helper method:** The [<service\_name>!SPCS\_GET\_EVENTS](/sql-reference/functions/spcs_get_events) table function returns events collected by Snowflake from the containers of the specified service.

  The following list explains the advantages of using this table function:

  - You can retrieve events for a specific service.
  - You can retrieve events within a specified time range.
  - The caller doesn’t need access to the entire events table, which can be beneficial for customers with strict information security requirements.

  The following SELECT statement uses the table function to retrieve platform events for the specified service recorded in the past hour:

  Copy code

  ```
  SELECT *
  FROM TABLE(mydb.myschema.echo_service!SPCS_GET_EVENTS(START_TIME => DATEADD('hour', -1, CURRENT_TIMESTAMP())));
  ```
- **Using the event table directly:** You can query the event table directly. To find the active event table for the account, use the [SHOW PARAMETERS](/sql-reference/sql/show-parameters) command to check the value of the [EVENT\_TABLE](/sql-reference/parameters#label-event-table) parameter:

  Copy code

  ```
  SHOW PARAMETERS LIKE 'event_table' IN ACCOUNT;
  ```

  The parameter specifies the active event table for the account.

  Next, query that event table. The following SELECT statement retrieves platform events for the specified service that was recorded in the past hour:

  Copy code

  ```
  SELECT TIMESTAMP, RESOURCE_ATTRIBUTES, RECORD, VALUE
    FROM <your_event_table>
    WHERE TIMESTAMP > DATEADD(hour, -1, CURRENT_TIMESTAMP())
   AND RESOURCE_ATTRIBUTES:"snow.service.name" = '<your_service_name>'
   AND RECORD_TYPE = 'EVENT'
   AND SCOPE:"name" = 'snow.spcs.platform'
    ORDER BY TIMESTAMP DESC
    LIMIT 10;
  ```

  For more information about event tables, see [Using event table](#label-snowpark-containers-working-with-services-using-event-table).

  The following columns in the event table provide useful information about the platform events:

  - **TIMESTAMP:** Shows when the event was recorded.
  - **RESOURCE\_ATTRIBUTES:** Provides a JSON object with metadata about the event source, such as a service, a container, or a compute pool. The following example of a value in the `resource_attribute` column identifies a specific service for which the event is recorded

    Copy code

    ```
    {
      "snow.compute_pool.name": "TUTORIAL_COMPUTE_POOL",
      "snow.compute_pool.id": 123,
      "snow.database.name": "TUTORIAL_DB",
      "snow.database.id": 456,
      "snow.schema.name": "DATA_SCHEMA",
      "snow.schema.id": 789,
      "snow.service.container.name": "echo",
      "snow.service.name": "ECHO_SERVICE2",
      "snow.service.id": 212,
      "snow.service.type": "Service"
    }
    ```
  - **SCOPE:** Indicates the origin of the event. For platform events, the name of the scope is `snow.spcs.platform`, as shown in the following example:

    Copy code

    ```
    { "name": "snow.spcs.platform" }
    ```
  - **RECORD\_TYPE:** For platform events, EVENT is the RECORD\_TYPE.
  - **RECORD:** Provides metadata about the specific event. The following metadata shows the name and severity level of the platform event:

    Copy code

    ```
    { "name": "CONTAINER.STATUS_CHANGE", "severity_text": "INFO" }
    ```
  - **VALUE:** Provides the event details. The following example shows the status and a message about the status of the container:

    Copy code

    ```
    { "message": "Running", "status": "READY" }
    ```

### Supported events

Snowflake records status change events for services (including job services), service instances, and containers, as well as service property change events.

The following table lists the platform events that Snowflake records. `RECORD` and `VALUE` in the column names refer to the columns in the event table (explained in the preceding section).

| RECORD:name | RECORD:severity\_text | VALUE:message | VALUE:status |
| --- | --- | --- | --- |
| SERVICE.STATUS\_CHANGE | INFO | Service is pending / Job is pending | PENDING |
| SERVICE.STATUS\_CHANGE | INFO | Service is resuming | RESUMING |
| SERVICE.STATUS\_CHANGE | INFO | Service is ready / Job is running | RUNNING |
| SERVICE.STATUS\_CHANGE | INFO | Service is suspending | SUSPENDING |
| SERVICE.STATUS\_CHANGE | INFO | Service has suspended | SUSPENDED |
| SERVICE.STATUS\_CHANGE | INFO | Service is upgrading | UPGRADING |
| SERVICE.STATUS\_CHANGE | INFO | Service has been upgraded | UPGRADED |
| SERVICE.STATUS\_CHANGE | INFO | Service is restoring snapshot <snapshot> on volume <volume> for instances [<instances>] | RESTORING\_SNAPSHOT |
| SERVICE.STATUS\_CHANGE | INFO | Service is deleting / Job is deleting | DELETING |
| SERVICE.STATUS\_CHANGE | INFO | Service has been deleted / Job has been deleted | DELETED |
| SERVICE.STATUS\_CHANGE | ERROR | Service has failed / Job has failed | FAILED |
| SERVICE.STATUS\_CHANGE | ERROR | Service has encountered an error / Job has encountered an error | INTERNAL\_ERROR |
| SERVICE.STATUS\_CHANGE | INFO | Job is completed | DONE |
| SERVICE.STATUS\_CHANGE | INFO | Job is being canceled | CANCELLING |
| SERVICE.STATUS\_CHANGE | INFO | Job has been canceled | CANCELLED |
| SERVICE.PROPERTY\_CHANGE | INFO | Set Service Properties [<property\_list>] |  |
| SERVICE.PROPERTY\_CHANGE | INFO | Unset Service Properties [<property\_list>] |  |
| SERVICE.PROPERTY\_CHANGE | INFO | Set Service tag(s) [<tag\_list>] |  |
| SERVICE.PROPERTY\_CHANGE | INFO | Unset Service tag(s) [<tag\_list>] |  |
| SERVICE\_INSTANCE.STATUS\_CHANGE | INFO | Service instance is pending / Job instance is pending | PENDING |
| SERVICE\_INSTANCE.STATUS\_CHANGE | INFO | Service instance is running / Job instance is running | READY |
| SERVICE\_INSTANCE.STATUS\_CHANGE | INFO | Service instance is terminating / Job instance is terminating | TERMINATING |
| SERVICE\_INSTANCE.STATUS\_CHANGE | INFO | Job instance has completed | SUCCEEDED |
| SERVICE\_INSTANCE.STATUS\_CHANGE | ERROR | Service instance failed / Job instance failed | FAILED |
| CONTAINER.STATUS\_CHANGE | INFO | Running | READY |
| CONTAINER.STATUS\_CHANGE | INFO | Readiness probe is failing at path: <path>, port: <port> | PENDING |
| CONTAINER.STATUS\_CHANGE | INFO | Waiting to start | PENDING |
| CONTAINER.STATUS\_CHANGE | INFO | Compute pool node(s) are being provisioned | PENDING |
| CONTAINER.STATUS\_CHANGE | ERROR | Failed to pull image | PENDING |
| CONTAINER.STATUS\_CHANGE | ERROR | Provided image name uses an invalid format | FAILED |
| CONTAINER.STATUS\_CHANGE | ERROR | Encountered fatal error, retrying | FAILED |
| CONTAINER.STATUS\_CHANGE | ERROR | Encountered fatal error | FAILED |
| CONTAINER.STATUS\_CHANGE | ERROR | Encountered fatal error while running, check container logs | FAILED |
| CONTAINER.STATUS\_CHANGE | ERROR | Container was OOMKilled due to resource usage | FAILED |
| CONTAINER.STATUS\_CHANGE | ERROR | User application error, check container logs | FAILED |
| CONTAINER.STATUS\_CHANGE | ERROR | Encountered fatal error while starting container | FAILED |
| CONTAINER.STATUS\_CHANGE | INFO | Completed successfully | DONE |

Expand

Show lessSee more

## Guidelines and limitations

- Maximum throughput for logs ingested to the event table per node is 1 MB/second for Snowflake accounts on AWS and Azure.
- Maximum combined throughput for metrics and traces ingested to the event table is 1 MB/second per node for both Azure and AWS.
- Maximum record size for logs ingested to the event table is 16 KiB.
