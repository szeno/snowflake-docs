# Snowflake Postgres metrics

Snowflake Postgres automatically collects instance metrics and stores them in your account’s active
[event table](/developer-guide/logging-tracing/event-table-setting-up). A monitoring agent
samples metrics approximately every 5 - 30 seconds depending on the metric type and writes them to
`SNOWFLAKE.TELEMETRY.EVENTS` with `RECORD_TYPE = 'METRIC'`.

You can query these metrics directly in Snowflake or forward them to an external observability
platform such as Grafana or Observe.

Note

For information about querying Postgres *log* data from the event table, see
[Snowflake Postgres logging](/user-guide/snowflake-postgres/postgres-logging).

## Available metrics

### Postgres metrics

| Metric | Type | Description |
| --- | --- | --- |
| `postgres_connections` | gauge | Number of active backend connections |
| `postgres_databases_size_bytes` | gauge | Total size of all databases (bytes) |
| `postgres_wal_size_bytes` | gauge | WAL directory size (bytes) |
| `postgres_log_size_bytes` | gauge | Log directory size (bytes) |
| `postgres_tmp_size_bytes` | gauge | Temp file size (bytes) |
| `postgres_locking_transactions` | gauge | Number of granted locks |
| `postgres_locked_transactions` | gauge | Number of waiting/blocked locks |
| `server_version` | gauge | Postgres version as an integer (for example, 180003 = 18.0.3) |

Expand

Show lessSee more

### Postgres process metrics

| Metric | Type | Unit | Dimensions |
| --- | --- | --- | --- |
| `process.cpu.time` | sum | seconds | state (user, system, wait) process.command, process.executable.name, process.owner, process.pid, process.parent\_pid |
| `process.memory.usage` | sum | bytes | process.command, process.executable.name, process.owner, process.pid, process.parent\_pid |
| `process.memory.virtual` | sum | bytes | process.command, process.executable.name, process.owner, process.pid, process.parent\_pid |

Expand

Show lessSee more

Note

Each Postgres process will have one `process.cpu.time` row for each CPU state and one for each of `process.memory.usage` and
`process.memory.virtual`.

The `process.*` dimension attributes are found in each row’s `resource_attributes` column. As with the `state` values for other
metrics, the `state` dimension attributes are in the `record_attributes` column.

### CPU metrics

| Metric | Type | Unit | Dimensions |
| --- | --- | --- | --- |
| `system.cpu.time` | sum | seconds | state: user, system, wait, idle, nice, interrupt, softirq, steal cpu: cpu# |
| `system.cpu.load_average.1m` | gauge | threads | — |
| `system.cpu.load_average.5m` | gauge | threads | — |
| `system.cpu.load_average.15m` | gauge | threads | — |

Expand

Show lessSee more

Note

Each cpu# (such as cpu0 and cpu2) will have one `system.cpu.time` row for each CPU state.

`system.cpu.time` is a cumulative counter. To get a percentage, compute the delta between
consecutive samples and divide by the elapsed interval.

### Memory metrics

| Metric | Type | Unit | Dimensions |
| --- | --- | --- | --- |
| `system.memory.usage` | sum | bytes | state: used, free, cached, buffered, slab\_reclaimable, slab\_unreclaimable |

Expand

Show lessSee more

Note

One `system.memory.usage` row for each state.

### Disk metrics

| Metric | Type | Unit | Dimensions |
| --- | --- | --- | --- |
| `system.filesystem.usage` | sum | bytes | mountpoint, device, state (used, free), type, mode |

Expand

Show lessSee more

Note

One `system.filesystem.usage` row for each state.

### Network metrics

| Metric | Type | Unit | Dimensions |
| --- | --- | --- | --- |
| `system.network.io` | sum | bytes | device, direction (transmit, receive) |

Expand

Show lessSee more

Note

Each device (‘eth0’ and ‘lo’) will have one `system.network.io` row for each direction.

### Paging metrics

| Metric | Type | Unit | Dimensions |
| --- | --- | --- | --- |
| `system.paging.usage` | sum | bytes | device, state (used, free) |

Expand

Show lessSee more

Note

One `system.paging.usage` row for each state.

## Resource attributes

Every metric row includes the following fields in `RESOURCE_ATTRIBUTES`:

| Attribute | Description | Example |
| --- | --- | --- |
| `instance_id` | Postgres instance identifier | `4jypgsndvzd5ta6ufaryx6owja` |
| `host_name` | Server host name | `df6m4y5m5fgfpb5idy2pj67xrm` |
| `host.id` | EC2 instance ID | `i-0f6724aef472706a3` |
| `host.type` | Instance family | `m8g.medium` |
| `cloud.region` | AWS region | `us-west-2` |
| `cloud.availability_zone` | Availability zone | `us-west-2b` |
| `application` | Always `postgres` | `postgres` |
| `os.type` | Always `linux` | `linux` |

Expand

Show lessSee more

## Querying metrics

A given Snowflake Postgres instance can have multiple servers running at any given time, such as a primary server and its HA server or
an upgrade replacement waiting for the instance’s maintenance window to be swapped into place. Since each of these servers will report
metrics for the instance’s given `instance_id` you also need the server `host_name` for the instance’s currently active server.

To find your Postgres instance’s `instance_id`, use [DESCRIBE POSTGRES INSTANCE](/sql-reference/sql/desc-postgres-instance):

Copy code

```
DESCRIBE POSTGRES INSTANCE my_instance
  ->> SELECT "value"
      FROM $1
      WHERE "property" = 'host';
```

The instance’s `instance_id` is the first segment of the returned `host` value (everything before the first period).

Note

You can use the `host` column of the SHOW POSTGRES INSTANCES command’s output to see the instance host values for all running Snowflake
Postgres instances on your account.

To find the instance’s current server `host_name`, use a simple DNS CNAME lookup of the instance’s `host` value.

Let’s say the returned `host` value was ’4jypgsndvzd5ta6ufaryx6owja.sfengineering-pgtest.preprod.us-west-2.aws.postgres.snowflake.app’
(so we know the instance’s `instance_id` is ’4jypgsndvzd5ta6ufaryx6owja’).

Here is an example using the `dig` CLI utility to do the DNS CNAME lookup:

Copy code

```
$ dig cname +short 4jypgsndvzd5ta6ufaryx6owja.sfengineering-pgtest.preprod.us-west-2.aws.postgres.snowflake.app
df6m4y5m5fgfpb5idy2pj67xrm.4jypgsndvzd5ta6ufaryx6owja.sfengineering-pgtest.preprod.us-west-2.aws.postgres.snowflake.app.
```

And here is an example using Python’s `dns.resolver` module:

Copy code

```
>>> import dns.resolver
>>> answer = dns.resolver.resolve('4jypgsndvzd5ta6ufaryx6owja.sfengineering-pgtest.preprod.us-west-2.aws.postgres.snowflake.app', 'CNAME')
>>> print(answer[0].target.to_text())
df6m4y5m5fgfpb5idy2pj67xrm.4jypgsndvzd5ta6ufaryx6owja.sfengineering-pgtest.preprod.us-west-2.aws.postgres.snowflake.app.
```

The `host_name` value is the first segment of that returned value, ‘df6m4y5m5fgfpb5idy2pj67xrm’ in the above examples.

The following query returns the most recent value for each metric collected in the last 5 minutes:

Copy code

```
SELECT TIMESTAMP as time,
  RECORD['metric']['name']::VARCHAR as metric,
  RESOURCE_ATTRIBUTES,
  RECORD_ATTRIBUTES,
  ROUND(VALUE::FLOAT, 2) AS value
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE RESOURCE_ATTRIBUTES['application'] = 'postgres'
  AND record_type = 'METRIC'
  AND RESOURCE_ATTRIBUTES['instance_id']::VARCHAR = '<your_instance_id>'
  AND RESOURCE_ATTRIBUTES['host_name']::VARCHAR = '<instance_current_host_name>'
  AND TIMESTAMP > CURRENT_TIMESTAMP() - INTERVAL '5 MINUTES'
QUALIFY ROW_NUMBER() OVER (PARTITION BY record, record_attributes ORDER BY timestamp desc, record, record_attributes) = 1
ORDER BY timestamp desc, metric, record_attributes;
```

Note

The above query uses the account default event table, `SNOWFLAKE.TELEMETRY.EVENTS`. If you’ve
set up a custom event table, adjust the query appropriately.

### Example metric queries

#### Active connections

Copy code

```
SELECT
    TIMESTAMP,
    VALUE::FLOAT AS connections
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE RECORD_TYPE = 'METRIC'
  AND RECORD['metric']['name']::VARCHAR = 'postgres_connections'
  AND RESOURCE_ATTRIBUTES['instance_id']::VARCHAR = '<your_instance_id>'
  AND RESOURCE_ATTRIBUTES['host_name']::VARCHAR = '<instance_current_host_name>'
  AND TIMESTAMP > CURRENT_TIMESTAMP() - INTERVAL '1 hour'
ORDER BY TIMESTAMP DESC;
```

#### Memory usage by state

Copy code

```
SELECT
    TIMESTAMP,
    RECORD_ATTRIBUTES['state']::VARCHAR AS state,
    ROUND(VALUE::FLOAT / (1024*1024*1024), 2) AS usage_gb
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE RECORD_TYPE = 'METRIC'
  AND RECORD['metric']['name']::VARCHAR = 'system.memory.usage'
  AND RECORD_ATTRIBUTES['state']::VARCHAR IN ('used', 'cached', 'buffered', 'free')
  AND RESOURCE_ATTRIBUTES['instance_id']::VARCHAR = '<your_instance_id>'
  AND RESOURCE_ATTRIBUTES['host_name']::VARCHAR = '<instance_current_host_name>'
  AND TIMESTAMP > CURRENT_TIMESTAMP() - INTERVAL '1 hour'
ORDER BY TIMESTAMP DESC;
```

#### CPU load averages

Copy code

```
SELECT
    TIMESTAMP,
    RECORD['metric']['name']::VARCHAR AS metric,
    VALUE::FLOAT AS load_avg
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE RECORD_TYPE = 'METRIC'
  AND RECORD['metric']['name']::VARCHAR IN (
      'system.cpu.load_average.1m',
      'system.cpu.load_average.5m',
      'system.cpu.load_average.15m'
  )
  AND RESOURCE_ATTRIBUTES['instance_id']::VARCHAR = '<your_instance_id>'
  AND RESOURCE_ATTRIBUTES['host_name']::VARCHAR = '<instance_current_host_name>'
  AND TIMESTAMP > CURRENT_TIMESTAMP() - INTERVAL '1 hour'
ORDER BY TIMESTAMP;
```

#### Database size

Copy code

```
SELECT
    TIMESTAMP,
    ROUND(VALUE::FLOAT / (1024*1024), 1) AS size_mb
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE RECORD_TYPE = 'METRIC'
  AND RECORD['metric']['name']::VARCHAR = 'postgres_databases_size_bytes'
  AND RESOURCE_ATTRIBUTES['instance_id']::VARCHAR = '<your_instance_id>'
  AND RESOURCE_ATTRIBUTES['host_name']::VARCHAR = '<instance_current_host_name>'
  AND TIMESTAMP > DATEADD('hour', -1, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC
LIMIT 1;
```

## Forwarding metrics to external tools

Because metrics are stored in a standard Snowflake table, you can forward them to any observability
platform that supports a Snowflake connection. For step-by-step setup with specific tools, see:

- [Monitor Snowflake Postgres with Grafana](https://www.snowflake.com/en/developers/guides/snowflake-postgres-monitoring-grafana/)
- [Monitor Snowflake Postgres with Observe](https://www.snowflake.com/en/developers/guides/snowflake-postgres-logs-to-observe/)
