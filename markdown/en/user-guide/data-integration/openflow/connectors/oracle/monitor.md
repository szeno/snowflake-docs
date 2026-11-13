# Monitor the Openflow Connector for Oracle

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

The Openflow Connector for Oracle is subject to the terms of service in the
[Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/).

The connector writes the metrics described on this page to your Openflow event table. A subset of these metrics is
also visualized in the [Openflow Connectors Dashboard](/user-guide/data-integration/openflow/connectors-dashboard).
For generic Openflow telemetry, see [Openflow telemetry](/user-guide/data-integration/openflow/monitor).

## Metrics

All metrics include the same
[resource](/user-guide/data-integration/openflow/monitor#label-openflow-event-table-resource-attributes) and
[connector](/user-guide/data-integration/openflow/monitor#label-openflow-connector-attributes) attributes as
application metrics. Table-level metrics also include
[table attributes](#label-openflow-db-table-attributes).
Some metrics also include additional attributes.

| Metric | Type | Resolution | Description |
| --- | --- | --- | --- |
| db.table.status | Gauge | Table | Current replication status of the table. Reported every 60 seconds for every table in replication. See [Replication status values](#label-openflow-db-table-status-values). |
| db.table.status.count | Gauge | Connector | Count of tables in each status. Reported every 60 seconds, as long as any tables are in replication. See [Replication status values](#label-openflow-db-table-status-values). |
| db.last.ingestion.time | Gauge | Table | Time when data was last written to the destination table, in milliseconds since the UNIX epoch. Reported every 60 seconds for up to 3 days after the last write, even when no new data arrives. |
| db.records.ingested | Counter | Table | Number of records written to Snowflake in each replication phase, indicated by the `db.replication.phase` attribute. In the `SNAPSHOT` phase, the value represents the number of records written to the destination table. In the `INCREMENTAL` phase, the value represents the number of records written to journal tables. Reported every 60 seconds for every table that received data since the last report. |
| db.commit.to.merge.latency | Gauge | Table | Highest time, in milliseconds, from when a change was committed in the source database until it was merged into the destination table. Reported every 60 seconds for every table that received data since the last report. |
| db.commit.to.capture.latency | Gauge | Connector | Highest time, in milliseconds, from when a change was committed in the source database until the connector read it. Reported every 60 seconds while the connector receives data. |
| db.capture.to.journal.latency | Gauge | Connector | Highest time, in milliseconds, from when the connector read a change until it was written to the journal table in Snowflake. Reported every 60 seconds while the connector receives data. |

Expand

Show lessSee more

Table-level metrics support up to 75,000 tables in a
single runtime. Above that limit, metrics might be lost.

### How the latency metrics relate

A change passes through three consecutive stages: the connector captures it from the source database, writes it
to the journal table, and then merges it into the destination table. Two of the latency metrics each cover one
stage, and the third covers the whole path:

- Capture latency (`db.commit.to.capture.latency`) covers the time until the connector reads the change.
- Flow processing time (`db.capture.to.journal.latency`) covers the time from when the connector reads the change event until it’s written to the journal table.
- End-to-end latency (`db.commit.to.merge.latency`) covers all three stages, until the change is merged into the destination table.

The merge stage doesn’t have its own metric. It includes the wait for the next scheduled merge and the execution
of the merge query.

![A change is committed in the source database, captured by the connector, written to the journal table, and merged into the destination table. Capture latency spans commit to capture, flow processing time spans capture to journal write, and merge time spans the wait for the scheduled merge and the merge query. End-to-end latency spans all three and is approximately their sum.](/static/images/openflow/openflow-db-connector-latency-metrics.svg)

Each latency metric reports the highest value in each 1-minute reporting interval. Because these are maximums, and
the end-to-end latency is reported per table while the other two are reported per connector, the
values don’t add up exactly. If the end-to-end latency is much higher than the sum of the capture latency and flow
processing time, most of the delay is in the merge stage. In that case, check the **Merge Task Schedule CRON**
connector parameter and the warehouse that runs the merge queries.

### Source object attributes

Table-level metrics identify the source table with the
following record attributes:

| Attribute | Description |
| --- | --- |
| source.database.name | Name of the source database. |
| source.schema.name | Name of the source schema. |
| source.table.name | Name of the source table. |

Expand

Show lessSee more

### Replication status values

The `db.table.status` metric encodes the replication status of a table as a number. The mapping is as follows:

| Value | Name | Description |
| --- | --- | --- |
| 0 | - | The table is no longer replicated, for example because it was removed from replication. Reported once. |
| 1 | NEW | The table is scheduled for replication, but replication hasn’t started. |
| 2 | SNAPSHOT\_REPLICATION | The connector is copying the existing data of the table. |
| 3 | INCREMENTAL\_REPLICATION | The connector is replicating changes. |
| 4 | FAILED | Replication has permanently stopped for an unknown reason. |
| 4001 | COMMUNICATION\_FAILURE | The connector failed to communicate with the source database. |
| 4003 | INVALID\_FETCH\_STRATEGY | The fetch strategy for the table is invalid or unsupported. |
| 4004 | OVERSIZED\_VALUE | A column value exceeds the maximum allowed size. |
| 4005 | MERGE\_QUERY\_FAILED | The merge query in Snowflake failed after the maximum number of retries. |
| 4006 | MERGE\_QUERY\_UNKNOWN\_STATUS | The merge query in Snowflake returned an unknown status. |
| 4008 | MISSING\_PRIMARY\_KEYS | The table can't be replicated without a primary key. |
| 4009 | MISSING\_REQUIRED\_ATTRIBUTES | A FlowFile is missing required attributes, or has invalid values for them. |
| 4010 | MISSING\_ROWID\_RANGE | No ROWID range was provided. |
| 4011 | NO\_COLUMNS\_IN\_TABLE | The source table has no columns. |
| 4012 | NO\_SCHEMA\_NAME\_PROVIDED | No schema name was provided. |
| 4013 | NO\_TABLE\_NAME\_PROVIDED | No table name was provided. |
| 4015 | REMOVED\_FROM\_REPLICATION | The table was removed from the source database, no longer matches the table filter, or is in a permanently failed state. |
| 4016 | SCHEMA\_CONVERSION\_ERROR | The table schema couldn’t be converted to the expected format. |
| 4017 | SCHEMA\_NOT\_FOUND | The schema of the table couldn't be found. |
| 4019 | SNOWFLAKE\_OBJECT\_OPERATION\_FAILED | The connector failed to create, update, or manage a Snowflake object. |
| 4020 | SNOWPIPE\_UPLOAD\_FAILED | The connector failed to upload data with Snowpipe Streaming. |
| 4021 | VALUE\_MAPPING\_ERROR | A value couldn't be mapped during data transformation. |
| 4022 | FLOWFILE\_READ\_ERROR | FlowFile content couldn’t be read or parsed. |
| 4024 | SNOWPIPE2\_UPLOAD\_FAILED | Snowflake rejected data sent with Snowpipe Streaming because of invalid record content. |
| 4025 | SCHEMA\_RECONCILE\_FAILED | Before a new snapshot, the connector failed to reconcile the destination table schema with the source table schema. |
| 4026 | CLONE\_TO\_ARCHIVE\_FAILED | Before a new snapshot, the connector failed to clone the destination table to its archive. |
| 4027 | TRUNCATE\_DESTINATION\_FAILED | Before a new snapshot, the connector failed to clear the destination table. |
| 4030 | REPLICATION\_KEY\_INVALIDATED | A replication key column was dropped or renamed. Update the key configuration, and then remove the table from replication and add it again. |
| 4031 | LOGICAL\_KEY\_CONFIG\_INVALID | The user-defined logical key configuration is invalid. For example, the key references a column that doesn't exist, contains duplicate columns, or is empty. Correct the table key configuration. |
| 4046 | LOGICAL\_KEY\_BEFORE\_IMAGE\_MISSING | A change didn't include the previous values of all logical key columns, because supplemental logging in the source database doesn't cover the logical key. Add supplemental logging for the logical key columns, and then remove the table from replication and add it again. |

Expand

Show lessSee more

Values of 4001 and higher mean that replication has permanently stopped for the listed reason.

## Alerts

The following alert templates in the **OPENFLOW** template group are specific to this connector:

| Template | Description | Settings |
| --- | --- | --- |
| **Table replication failure alert** | Fires for each table whose replication failed during the lookback window. Can be configured for the account, a deployment, a runtime, or a connector. | - **Lookback window (hours)**: Default: *1*. - **Table names filter**: Optional. A comma-separated list of the tables to monitor.   Leave empty to monitor all tables. |
| **Openflow data staleness alert** | Fires for each of the specified tables when no new data was written to its destination table for longer than the staleness threshold. Can be configured for the account, a deployment, a runtime, or a connector. | - **Table names filter**: Required. A comma-separated list of the tables to monitor. - **Staleness threshold (hours)**: Default: *4*. - **Lookback window (hours)**: Default: *6*. |

Expand

Show lessSee more

For more information and generic Openflow alerts, see [Set up alerts for Openflow](/user-guide/data-integration/openflow/alerts).

## Example queries

The following queries assume that Openflow sends telemetry to the default event table,
`SNOWFLAKE.TELEMETRY.EVENTS`. If you use a different event table, substitute its name.

### Find replication failures

This query returns the tables whose latest status in the last hour is failed:

Copy code

```
SELECT
  record_attributes:"connector.name"::STRING AS connector,
  record_attributes:"source.database.name"::STRING AS source_database,
  record_attributes:"source.schema.name"::STRING AS source_schema,
  record_attributes:"source.table.name"::STRING AS source_table,
  value::NUMBER AS status,
  timestamp
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE timestamp > DATEADD(hour, -1, SYSDATE())
  AND record_type = 'METRIC'
  AND record:metric:name = 'db.table.status'
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY connector, source_database, source_schema, source_table
    ORDER BY timestamp DESC) = 1
  AND status >= 4;
```

### Find destination tables without recent data

This query returns the tables that had no data written to the destination table in
the last hour. A table without changes in the source database also appears in the
results.

Copy code

```
SELECT
  record_attributes:"connector.name"::STRING AS connector,
  record_attributes:"source.database.name"::STRING AS source_database,
  record_attributes:"source.schema.name"::STRING AS source_schema,
  record_attributes:"source.table.name"::STRING AS source_table,
  TO_TIMESTAMP_LTZ(MAX(value::NUMBER), 3) AS last_ingestion_time
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE timestamp > DATEADD(hour, -2, SYSDATE())
  AND record_type = 'METRIC'
  AND record:metric:name = 'db.last.ingestion.time'
GROUP BY connector, source_database, source_schema, source_table
HAVING last_ingestion_time < DATEADD(hour, -1, CURRENT_TIMESTAMP());
```

### Plot replication latency over time

This query returns the latency from source commit to destination table for each
table over the last 24 hours. To
plot it, show the results as a line chart with `timestamp` on the X-axis and `latency_seconds` on the Y-axis.

Copy code

```
SELECT
  timestamp,
  record_attributes:"connector.name"::STRING AS connector,
  record_attributes:"source.database.name"::STRING AS source_database,
  record_attributes:"source.schema.name"::STRING AS source_schema,
  record_attributes:"source.table.name"::STRING AS source_table,
  value::NUMBER / 1000 AS latency_seconds
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE timestamp > DATEADD(day, -1, SYSDATE())
  AND record_type = 'METRIC'
  AND record:metric:name = 'db.commit.to.merge.latency'
ORDER BY timestamp;
```

### Count records written per replication phase

This query returns the number of records written for each table per hour and replication phase in the last 24 hours:

Copy code

```
SELECT
  DATE_TRUNC(hour, timestamp) AS hour,
  record_attributes:"connector.name"::STRING AS connector,
  record_attributes:"source.database.name"::STRING AS source_database,
  record_attributes:"source.schema.name"::STRING AS source_schema,
  record_attributes:"source.table.name"::STRING AS source_table,
  record_attributes:"db.replication.phase"::STRING AS phase,
  SUM(value::NUMBER) AS records
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE timestamp > DATEADD(day, -1, SYSDATE())
  AND record_type = 'METRIC'
  AND record:metric:name = 'db.records.ingested'
GROUP BY hour, connector, source_database, source_schema, source_table, phase
ORDER BY hour, connector, source_schema, source_table;
```
