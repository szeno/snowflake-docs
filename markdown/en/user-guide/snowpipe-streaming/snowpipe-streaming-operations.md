# Operations and reference

This topic covers monitoring, observability, and access privileges for Snowpipe Streaming with high-performance architecture.

## Monitoring and observability

You can monitor ingestion status through the [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY](/sql-reference/account-usage/snowpipe_streaming_channel_history) view in Snowsight and the `GET_CHANNEL_STATUS` API. These provide insight into channel state, offset progress, and ingestion health.

## Required access privileges

Calling the Snowpipe Streaming API requires a role with the following privileges:

| Object | Privilege |
| --- | --- |
| Table | OWNERSHIP or a minimum of INSERT and EVOLVE SCHEMA (only required when using schema evolution for Kafka connector with Snowpipe Streaming) |
| Database | USAGE |
| Schema | USAGE |
| Pipe | OPERATE |

Expand

Show lessSee more
