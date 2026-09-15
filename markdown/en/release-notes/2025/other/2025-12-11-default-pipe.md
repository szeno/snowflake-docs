# Dec 11, 2025: Default pipe for Snowpipe Streaming with high-performance architecture

We are enhancing the high-performance Snowpipe Streaming architecture by introducing the default pipe capability.

This feature simplifies the data ingestion process by eliminating the need for you to create a pipe manually by using CREATE PIPE DDL statements. With this change, users can initiate streaming immediately against a target table. The default pipe is implicitly available for any table designed to receive streaming data.

The default pipe is system-generated and follows a specific naming convention that is derived from its target table:

| Attribute | Format | Example |
| --- | --- | --- |
| Default Pipe Name | `<TABLE_NAME>-STREAMING` | If your target table is named `MY_TABLE`, the default pipe is named `MY_TABLE-STREAMING`. |

Expand

Show lessSee more

The default pipe is entirely managed by Snowflake and has system-defined metadata; for example, its OWNER attribute is NULL.

When you configure the Snowpipe Streaming Client SDK, or REST API, you can reference this default pipe name in your client configuration to target the destination table directly.

For more information, see [Snowpipe Streaming key concepts](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview).
