# Apr 8, 2026: Error logging for Snowpipe Streaming (*General availability*)

With this release, error logging for Snowpipe Streaming with high-performance architecture is now generally
available. When error logging is turned on for a target table, rows that fail server-side processing are
automatically captured in a dedicated error table instead of being silently dropped. This feature includes
the following capabilities:

- Row-level error capture with full original payloads and detailed error metadata.
- Filtering by Snowpipe Streaming errors using the `error_metadata:service` field.
- Querying, analyzing, and reprocessing failed rows using standard SQL.

Turning on error logging doesn’t change your Snowpipe Streaming ingestion costs. Snowflake charges for
data stored in the error table at the standard storage rate.

For more information, see [Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).
