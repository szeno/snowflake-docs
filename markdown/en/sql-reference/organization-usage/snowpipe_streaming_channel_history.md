[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view provides a historical record of pipeline errors, enabling users to monitor performance trends. This view displays key metrics such as processed data volume, error rates, and latency.

You can use this Organization Usage view to query the error history for a specific pipe or channel.

Note

The SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY view only applies to [Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview).

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time when the rowset channel history was created. |
| CHANNEL\_ID | NUMBER | The internal, system-generated ID of the Snowpipe Streaming channel. |
| CHANNEL\_NAME | VARCHAR | The user-defined name of the Snowpipe Streaming channel. |
| PIPE\_ID | NUMBER | The internal ID of the Snowpipe object associated with this Snowpipe Streaming channel. |
| END\_OFFSET | VARCHAR | The last offset token processed and included in this specific channel history record. |
| TABLE\_ID | NUMBER | The internal ID of the target table for this Snowpipe Streaming channel. |
| TABLE\_NAME | VARCHAR | The name of the target table for this Snowpipe Streaming channel. |
| TABLE\_SCHEMA\_ID | NUMBER | The internal ID of the schema containing the target table. |
| TABLE\_SCHEMA\_NAME | VARCHAR | The name of the schema containing the target table. |
| TABLE\_DATABASE\_ID | NUMBER | The internal ID of the database containing the target table. |
| TABLE\_DATABASE\_NAME | VARCHAR | The name of the database containing the target table. |
| PIPE\_NAME | VARCHAR | “The name of the Snowpipe object associated with the current Snowpipe Streaming channel history entry. |
|  |  |  |
| Named pipes: The value is the user-defined name of the Snowpipe object associated with the channel. |  |  |
|  |  |  |
| Default pipe: The value is automatically derived from the target table name; for example, MY\_TABLE-STREAMING.” |  |  |
| PIPE\_SCHEMA\_ID | NUMBER | “The internal identifier for the schema associated with the Snowpipe Streaming channel. |
|  |  |  |
| Named pipes: The value is the internal ID of the schema that contains the user-defined Snowpipe object. |  |  |
|  |  |  |
| Default pipe: The value is the internal ID of the schema that contains the target table.” |  |  |
| PIPE\_SCHEMA\_NAME | VARCHAR | “The name of the schema associated with the Snowpipe Streaming channel. |
|  |  |  |
| Named pipes: The value is the user-defined name of the schema that contains the Snowpipe object. |  |  |
|  |  |  |
| Default pipe: The value is the name of the schema that contains the target table.” |  |  |
| PIPE\_DATABASE\_ID | NUMBER | “The internal identifier for the database associated with the Snowpipe Streaming channel. |
|  |  |  |
| Named pipes: The value is the internal ID of the database that contains the user-defined Snowpipe object. |  |  |
|  |  |  |
| Default pipe: The value is the internal ID of the database that contains the target table.” |  |  |
| PIPE\_DATABASE\_NAME | VARCHAR | “The name of the database associated with the Snowpipe Streaming channel. |
|  |  |  |
| Named pipes: The value is the user-defined name of the database that contains the Snowpipe object. |  |  |
|  |  |  |
| Default pipe: The value is the name of the database that contains the target table.” |  |  |
| LAST\_ERROR\_OFFSET\_UPPER\_BOUND | VARCHAR | The upper bound of the offset token range of the last rowset that encountered errors during this historical period. |
| LAST\_ERROR\_MESSAGE | VARCHAR | The last error message encountered while writing data to the channel. This column displays a redacted error message when an error is encountered. |
| SNOWFLAKE\_PROCESSING\_LATENCY\_MS | NUMBER | The average latency, in milliseconds, observed by the Snowflake service in processing rowsets for this channel during this historical period. |
| ROWS\_INSERTED | NUMBER | The total number of rows successfully inserted through this channel during this historical period. |
| ROWS\_PARSED | NUMBER | The total number of rows parsed (processed) by the channel during this historical period. |
| ROW\_ERROR\_COUNT | NUMBER | The total number of rows that encountered errors and were not inserted through this channel during this historical period. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 5 hours.
- The Snowpipe Streaming high-performance architecture only supports ON\_ERROR=CONTINUE. Other ON\_ERROR options are not supported.
