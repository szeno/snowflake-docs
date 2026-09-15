# Troubleshoot the Snowflake Connector for Kafka

This topic describes how to troubleshoot common issues with the Snowflake Connector for Kafka.

## Ingestion errors

### Channel reports increasing rows\_error\_count

If the Snowpipe Streaming channel reports an increasing `rows_error_count`, the connector
behavior depends on the `errors.tolerance` setting:

- With `errors.tolerance=none` (default), the connector task fails with `ERROR_5030`.
- With `errors.tolerance=all`, the connector continues but logs the error count.

Note

With server-side validation and `errors.tolerance=none`, errors are asynchronous. The
connector detects the error on the next pre-commit cycle, so some additional records may be
ingested before the task fails.

To investigate:

1. Check the Error Table associated with your target table to identify the failing records.
   See [Error handling in Snowpipe Streaming high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-error-handling) for details.
2. Use the gap-finding technique described in [Detect and recover from errors using metadata offsets](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-best-practices#label-detect-and-recover-from-errors-using-metadata-offsets)
   with Kafka offset information from the `RECORD_METADATA` column.
3. Review the connector logs for error details (enable `errors.log.enable=true` for verbose logging).

### Connector task fails with ERROR\_5030

`ERROR_5030` indicates that the connector detected a data ingestion error.
Common causes include:

- Data type mismatches between the Kafka record and the target table schema.
- A user-created pipe exists while `snowflake.validation=client_side` is configured.
  Client-side validation only works with the default pipe.
- Schema changes in the Kafka records that can’t be automatically evolved.

To resolve:

1. Review the error message and connector logs for the specific cause.
2. If using client-side validation with a user-defined pipe, switch to `snowflake.validation=server_side`
   or remove the user-defined pipe.
3. Fix the data in the source Kafka topic or adjust the target table schema.

### Schema evolution issues

Warning

With server-side validation (the default), the connector infers column types from the first observed record values and does not use a schema registry, so an inferred type can differ from the declared type. For example:

- A field declared as `FLOAT64` (double) in a schema registry can be inferred as `NUMBER(38,0)` if the first records carry whole numbers with no fractional digits, which silently truncates the decimal portion of all later values.
- Binary columns can’t be inferred, and a string like `"2026-04-13"` can be interpreted as DATE instead of TEXT.

These changes are not recoverable after ingestion begins. If your source uses a schema registry or a strongly typed schema (for example, Avro or Protobuf), use client-side validation.

If schema evolution produces unexpected column types:

- Use client-side validation (`snowflake.validation=client_side`), which creates columns from the declared schema-registry types. For more information, see [Validation modes](/user-guide/kafka-connector/validation-error-handling#label-kafkahp-choosing-validation-mode).
- Pre-create the table with the correct schema before starting the connector.

Note

The connector only caches the table schema. Concurrent DDL operations on the target table
while the connector is running may cause undefined behavior. Avoid running DDL on tables
that the connector is actively ingesting into.

## Connection and authentication issues

### Authentication failures

The v4 connector supports key-pair authentication only. Common authentication issues:

- **Invalid private key**: Verify that the `snowflake.private.key` value is a valid Base64-encoded
  PKCS#8 private key.
- **Key passphrase**: If your key is encrypted, set `snowflake.private.key.passphrase` to the correct passphrase.
- **Role privileges**: Verify that the role specified in `snowflake.role.name` has the required
  privileges. See [Snowflake Connector for Kafka: Configure Snowflake](/user-guide/kafka-connector/setup-snowflake) for details.

### Authorization errors

If the connector encounters authorization errors from Snowflake, the behavior depends on the
`enable.task.fail.on.authorization.errors` setting:

- With `enable.task.fail.on.authorization.errors=false` (default), the connector retries.
- With `enable.task.fail.on.authorization.errors=true`, the connector task fails immediately.

## Configuration issues

### Unsupported converter with schematization

When `snowflake.enable.schematization=true` (the default), the `StringConverter` and
`ByteArrayConverter` aren’t supported as value converters. Use structured converters instead:

- `org.apache.kafka.connect.json.JsonConverter`
- `io.confluent.connect.avro.AvroConverter`
- `io.confluent.connect.protobuf.ProtobufConverter`

### Removed v3 configuration properties

If you see errors about unrecognized configuration properties, check whether you’re using
properties that were removed in v4. See [Migrate from Kafka connector v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4) for the full list of
removed configurations.

### Compatibility validator failures at startup

If the connector fails at startup with errors about missing or incompatible configuration values,
the compatibility validator (`snowflake.streaming.validate.compatibility.with.classic`) is
checking your config against v3 migration requirements.

- **For new installations**: Set `snowflake.streaming.validate.compatibility.with.classic=false`
  to skip the check.
- **For migrations from v3**: Set all the required compatibility properties explicitly.
  See [snowflake.streaming.validate.compatibility.with.classic](/user-guide/kafka-connector/setup-kafka#label-kafkahp-compatibility-validator) for the full list.

## Performance issues

### Ingestion lag growing

If the `latest-consumer-offset` minus `persisted-in-snowflake-offset` gap is increasing
(visible through [JMX metrics](/user-guide/kafka-connector/monitor)), the connector is falling behind.

To resolve:

- **Increase tasks**: Set `tasks.max` closer to the total number of Kafka partitions. Optimal
  performance is typically 2 tasks per CPU core across the Kafka Connect cluster.
- **Check backpressure**: If the `backpressure-rewind-count` metric is increasing, the Snowpipe
  Streaming SDK is at capacity. Consider scaling out your Kafka Connect cluster.
- **Review JVM memory**: Limit JVM heap to approximately 50% of available memory. The Rust-based
  Snowpipe Streaming SDK uses off-heap memory for buffering, which isn’t managed by the JVM.

### Table and pipe caching

The connector caches table and pipe existence checks to reduce database queries. If you
encounter issues with the connector not detecting newly created tables or pipes,
adjust the cache expiration time:

Copy code

```
snowflake.cache.table.exists.expire.ms=60000
snowflake.cache.pipe.exists.expire.ms=60000
```

### Sustained channel recovery

Occasional channel recoveries are normal. However, if the `channel-recovery-count` metric
is continuously increasing, it may indicate:

- Schema changes on the target table that conflict with the connector’s cached schema.
- Permission changes that affect the connector’s role.
- Network instability between the Kafka Connect cluster and Snowflake.

Review the connector logs for specific recovery reasons.

### SDK client leak

If the `sdk-client-count` JMX metric grows continuously, the connector may be leaking
Snowpipe Streaming SDK clients. Each distinct target table should have one SDK client.
If the count exceeds the number of distinct tables, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Migration issues

### SSv1 channel not found during offset migration

If the connector fails with a channel-not-found error when using
`snowflake.streaming.classic.offset.migration=strict`:

- Verify that you’re using the same connector name as your v3 deployment.
- Check whether `snowflake.streaming.classic.offset.migration.include.connector.name` matches
  your v3 setting for `snowflake.streaming.channel.name.include.connector.name`.
- Switch to `best_effort` mode if the channel has already been cleaned up, or if you’re adding
  new topics that didn’t exist in v3.

### Duplicates after migration

If you see duplicate records after migrating from v3:

- Verify that `RECORD_METADATA` contains topic, partition, and offset fields.
- Use the deduplication query in [Downgrading from v4 to v3](/user-guide/kafka-connector/migrate-v3-to-v4#label-downgrade-v4-to-v3) to remove duplicates.

## Logging

The Snowpipe Streaming SDK can produce verbose logs. To reduce log noise, set the following
environment variable on your Kafka Connect workers:

Copy code

```
export SS_LOG_LEVEL=warn
```

For detailed connector logging with context, configure the log pattern:

Copy code

```
CONNECT_LOG4J_APPENDER_STDOUT_LAYOUT_CONVERSIONPATTERN="[%d] %p %X{connector.context}%m (%c:%L)%n"
```

## Report issues

For issues not covered by this guide, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
