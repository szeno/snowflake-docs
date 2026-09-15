# Monitor the Openflow Connector for Salesforce Bulk API

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

The connector writes information about completed Salesforce Bulk API jobs to logs in the event table. You can query these logs to track the objects and number of records replicated to Snowflake.

The examples on this page query `OPENFLOW.TELEMETRY.EVENTS`. If your Openflow deployment sends telemetry to a different event table, replace the table name in the examples. Adjust the 30-minute time range as needed.

## Query replication activity

By default, the connector logs the Salesforce object type, number of records processed, bulk job ID, and system modification timestamp. Use the following query when **Enable Merge Metrics** is set to `false`:

Copy code

```
WITH connector_logs AS (
  SELECT
    timestamp,
    resource_attributes:"openflow.dataplane.id"::VARCHAR AS deployment_id,
    resource_attributes:"k8s.namespace.name"::VARCHAR AS runtime_key,
    TRY_PARSE_JSON(value) AS parsed_log
  FROM OPENFLOW.TELEMETRY.EVENTS
  WHERE timestamp >= DATEADD('minutes', -30, CURRENT_TIMESTAMP())
    AND record_type = 'LOG'
    AND resource_attributes:"k8s.namespace.name"::VARCHAR LIKE 'runtime-%'
),
salesforce_logs AS (
  SELECT
    timestamp,
    deployment_id,
    runtime_key,
    parsed_log:formattedMessage::VARCHAR AS message
  FROM connector_logs
  WHERE parsed_log:loggerName::VARCHAR = 'org.apache.nifi.processors.standard.LogMessage'
    AND CONTAINS(parsed_log:formattedMessage::VARCHAR, 'SALESFORCE_BULK_API - ')
)
SELECT
  timestamp,
  deployment_id,
  runtime_key,
  TRIM(REGEXP_SUBSTR(message, 'ObjectType = ([^;]+)', 1, 1, 'e', 1)) AS object_type,
  TRY_TO_NUMBER(TRIM(REGEXP_SUBSTR(message, 'Records = ([^;]+)', 1, 1, 'e', 1))) AS records,
  TRIM(REGEXP_SUBSTR(message, 'BulkJobID = ([^;]*)', 1, 1, 'e', 1)) AS bulk_job_id,
  TRIM(REGEXP_SUBSTR(message, 'SystemModstamp = ([^;]+)', 1, 1, 'e', 1)) AS system_modstamp
FROM salesforce_logs
ORDER BY timestamp DESC;
```

## Query merge metrics

Set **Enable Merge Metrics** to `true` to include detailed record counts in the logs. The connector runs an additional query before each incremental merge to calculate the counts. This query uses the warehouse configured in **Snowflake Warehouse**.

Merge metrics are available only for Salesforce objects that include the `IsDeleted` field. Use the following query to retrieve the replication activity and merge metrics:

Copy code

```
WITH connector_logs AS (
  SELECT
    timestamp,
    resource_attributes:"openflow.dataplane.id"::VARCHAR AS deployment_id,
    resource_attributes:"k8s.namespace.name"::VARCHAR AS runtime_key,
    TRY_PARSE_JSON(value) AS parsed_log
  FROM OPENFLOW.TELEMETRY.EVENTS
  WHERE timestamp >= DATEADD('minutes', -30, CURRENT_TIMESTAMP())
    AND record_type = 'LOG'
    AND resource_attributes:"k8s.namespace.name"::VARCHAR LIKE 'runtime-%'
),
salesforce_logs AS (
  SELECT
    timestamp,
    deployment_id,
    runtime_key,
    parsed_log:formattedMessage::VARCHAR AS message
  FROM connector_logs
  WHERE parsed_log:loggerName::VARCHAR = 'org.apache.nifi.processors.standard.LogMessage'
    AND CONTAINS(parsed_log:formattedMessage::VARCHAR, 'SALESFORCE_BULK_API - ')
)
SELECT
  timestamp,
  deployment_id,
  runtime_key,
  TRIM(REGEXP_SUBSTR(message, 'ObjectType = ([^;]+)', 1, 1, 'e', 1)) AS object_type,
  TRY_TO_NUMBER(TRIM(REGEXP_SUBSTR(message, 'Records = ([^;]+)', 1, 1, 'e', 1))) AS records,
  TRIM(REGEXP_SUBSTR(message, 'BulkJobID = ([^;]*)', 1, 1, 'e', 1)) AS bulk_job_id,
  TRIM(REGEXP_SUBSTR(message, 'SystemModstamp = ([^;]+)', 1, 1, 'e', 1)) AS system_modstamp,
  TRY_TO_NUMBER(TRIM(REGEXP_SUBSTR(message, 'ROWS_ADDED = ([^;]+)', 1, 1, 'e', 1))) AS rows_added,
  TRY_TO_NUMBER(TRIM(REGEXP_SUBSTR(message, 'ROWS_ADDED_DELETED = ([^;]+)', 1, 1, 'e', 1))) AS rows_added_deleted,
  TRY_TO_NUMBER(TRIM(REGEXP_SUBSTR(message, 'ROWS_UPDATED = ([^;]+)', 1, 1, 'e', 1))) AS rows_updated,
  TRY_TO_NUMBER(TRIM(REGEXP_SUBSTR(message, 'ROWS_DELETED = ([^;]+)', 1, 1, 'e', 1))) AS rows_deleted,
  TRY_TO_NUMBER(TRIM(REGEXP_SUBSTR(message, 'ROWS_RESTORED = ([^;]+)', 1, 1, 'e', 1))) AS rows_restored
FROM salesforce_logs
ORDER BY timestamp DESC;
```

The metrics have the following meanings:

| Metric | Initial load | Incremental load |
| --- | --- | --- |
| `ROWS_ADDED` | Records loaded that aren’t marked as deleted. | Active source records that don’t exist in the destination table. |
| `ROWS_ADDED_DELETED` | Records loaded that are already marked as deleted. | Source records marked as deleted that don’t exist in the destination table. |
| `ROWS_UPDATED` | `0` | Active source records that match active records in the destination table. |
| `ROWS_DELETED` | `0` | Source records marked as deleted that match active records in the destination table. |
| `ROWS_RESTORED` | `0` | Active source records that match records marked as deleted in the destination table. |

Expand

Show lessSee more

`ROWS_UPDATED` counts active source records that match active destination records. It doesn’t compare individual field values and doesn’t indicate whether a field value changed.

The merge metric columns in the query return `NULL` when the log doesn’t contain merge metrics. This occurs when **Enable Merge Metrics** is set to `false`, the Salesforce object doesn’t include the `IsDeleted` field, or the log was generated by an earlier connector version that didn’t support merge metrics.
