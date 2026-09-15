# Snowpipe Streaming high-performance architecture: Understand your costs

This document outlines the billing model for the new high-performance architecture of Snowpipe Streaming, designed for transparent and predictable pricing.

## Billing model: Throughput-based

The high-performance architecture introduces a flat-rate pricing model based on the volume of uncompressed data ingested.

- Rate: Charged per uncompressed gigabyte (GB). For the current rate, see the [Snowflake Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- Metering: Data is metered by the Snowpipe Streaming service during the ingestion process.
- Measurement basis: Billing is based on the input bytes received by Snowpipe Streaming, not the final byte count produced in the target table. This means the raw, uncompressed data volume sent to Snowpipe Streaming is what’s measured for billing.

Note

Snowflake charges only for the data values ingested, not for the structural elements such as keys. For instance, when ingesting a JSON file that contains both keys and values, billing is based solely on the byte size of the values. This is because the values represent the actual data being ingested, similar to how data in a CSV file (without headers explicitly included in the data charge) would be measured.

**Key change from Snowpipe Streaming Classic**: This new model differs significantly from the Snowpipe Streaming Classic billing, where credits are primarily based on serverless compute usage and active client connections.

### Billing example

Let’s consider an example where you are ingesting uncompressed data values at a rate of 1 megabyte per second (MB/s).

- Data Values Ingested per Second: 1 MB
- Data Values Ingested per Hour: 1 MB/s \* 3600 s/hour = 3600 MB/hour = 3.6 GB/hour (assuming 1 GB = 1000 MB for this billing context).
- Credits Consumed per Hour: 3.6 GB \* current rate per GB

For the exact credit calculation, see the current rate provided on the [Snowflake Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

### Monitoring your usage and costs

To understand the data ingested and the corresponding credits consumed within the high-performance architecture, you can query the ACCOUNT\_USAGE.METERING\_HISTORY view.

Here is an example:

Copy code

```
SELECT *
FROM snowflake.account_usage.metering_history m
JOIN snowflake.account_usage.pipes p
  ON m.entity_id = p.pipe_id
 AND m.name = p.pipe_name
 AND m.service_type = 'SNOWPIPE_STREAMING';
```

### Distinguishing costs: High-performance vs. Classic Snowpipe Streaming

It’s important to be able to differentiate costs originating from the new high-performance architecture versus the existing Snowpipe Streaming Classic model. You can achieve this by querying your billing history and filtering based on the service type or other distinguishing attributes.

### Snowpipe Streaming Classic credits

For information on the billing model for Snowpipe Streaming Classic, see [Costs for Snowpipe Streaming Classic](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-billing).
