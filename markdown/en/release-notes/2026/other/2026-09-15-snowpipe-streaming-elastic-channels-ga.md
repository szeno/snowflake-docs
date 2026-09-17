# Sep 15, 2026: Elastic Channels for Snowpipe Streaming (*General availability*)

Elastic Channels for Snowpipe Streaming are now generally available. Elastic Channels provide one implicit, server-scaled ingestion path per pipe, so concurrent producers can stream directly to Snowflake tables and supported Snowflake-managed Iceberg tables without managing channel names, lifecycle, ordering, or offset tokens.

The GA release includes:

- At-least-once ingestion with per-append durable acknowledgements.
- Fire-and-forget and waitable append methods in the Java, Python, and Node.js SDKs.
- Success and error callbacks with caller-supplied append tokens for outcome correlation.
- An Elastic table endpoint that automatically uses the managed default pipe, and an Elastic pipe endpoint for custom pipes.

Elastic Channels require Snowpipe Streaming SDK version 1.8.0 or later for the documented GA API. Use Named Channels when your application requires ordered, exactly-once ingestion or source-offset integration.

For more information, see the [Snowpipe Streaming overview](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview), [Elastic Channels overview](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-overview), and [SDK getting-started tutorial](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-getting-started).
